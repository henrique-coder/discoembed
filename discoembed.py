# Built-in modules
from http import HTTPStatus
from pathlib import Path
from typing import Union, Tuple

# Third-party modules
from flask import Flask, Response, request, jsonify, render_template_string
from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from orjson import loads as orjson_loads
from werkzeug.middleware.proxy_fix import ProxyFix

# Local modules
from static.data.functions import CacheTools, is_valid_url
from static.data.logger import logger


# Setup Flask application and debugging mode
app = Flask(__name__)

# Setup Flask cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
logger.info(f'Flask cache enabled. Cache type: {cache.config["CACHE_TYPE"]}')

# Setup Talisman for security headers
talisman = Talisman(app, content_security_policy={'default-src': ["'self'", 'https://cdnjs.cloudflare.com'], 'style-src': ["'self'", "'unsafe-inline'", 'https://cdnjs.cloudflare.com'], 'script-src': ["'self'", 'https://cdnjs.cloudflare.com']})
logger.info('Talisman security headers enabled')

# Setup Flask CSRF protection
CSRFProtect(app)
logger.info('CSRF protection enabled')

# Setup Flask Compress for GZIP compression
Compress(app)
logger.info('Response compression enabled')

# Setup Flask CORS
CORS(app, resources={r'*': {'origins': '*'}})
logger.info('CORS enabled')

# Setup proxy fix for the Flask application
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=0, x_proto=1, x_host=1, x_port=1, x_prefix=1)


# Function to create an embed HTML
def make_embed_html(url: str, cover: str, width: int = None, height: int = None) -> str:
    return f'<!DOCTYPE html><html lang="en"><head><meta property="og:video:url" content="{url}"><meta property="og:image" content="{cover}"><meta property="og:video:width" content="{width if width else ""}"><meta property="og:video:height" content="{height if height else ""}"><meta property="og:type" content="video.other"></head></html>'

# Setup API routes
@app.route('/', methods=['GET'])
@cache.cached(timeout=5, make_cache_key=CacheTools.gen_cache_key)
def index() -> Tuple[Union[Response, render_template_string], HTTPStatus]:
    logger.info(f'GET request received from ip {request.remote_addr} with user agent {request.user_agent}')

    if str(request.user_agent).strip() != r'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)':
        return jsonify({'error': 'Unauthorized access'}), HTTPStatus.UNAUTHORIZED

    # Get parameters from the URL
    url = request.args.get('url')
    cover = request.args.get('cover')
    width = request.args.get('width')
    height = request.args.get('height')

    # Check if the URL is valid
    if not url:
        return render_template_string(make_embed_html('https://i.imgur.com/k9FrlEe.mp4', 'https://i.imgur.com/bUNtIgQ.png', 1280, 720)), HTTPStatus.OK
    elif not is_valid_url(url, online_check=False):
        return render_template_string(make_embed_html('https://i.imgur.com/bMGv6H5.mp4', 'https://i.imgur.com/kTj9dnk.png', 1280, 720)), HTTPStatus.OK

    # Check if the cover is valid
    if not cover:
        cover = 'https://i.imgur.com/8ZkUMGK.png'
    elif not is_valid_url(cover, online_check=False):
        return render_template_string(make_embed_html(url, 'https://i.imgur.com/Cl6kMsz.png', width, height)), HTTPStatus.OK

    # Check if the width and height are valid
    try:
        width = int(width)
        height = int(height)
    except (TypeError, ValueError):
        width, height = 1920, 1080

    # Return the embed HTML
    return render_template_string(make_embed_html(url, cover, width, height)), HTTPStatus.OK


@app.route('/status', methods=['GET'])
def health() -> Tuple[Response, HTTPStatus]:
    return jsonify({'status': 'ok'}), HTTPStatus.OK


if __name__ == '__main__':
    # Load the configuration file
    current_path = Path(__file__).parent
    config_path = Path(current_path, 'config.json')
    config = orjson_loads(config_path.read_text())

    # Setting up Flask default configuration
    app.static_folder = Path(current_path, config['flask']['staticFolder'])
    app.template_folder = Path(current_path, config['flask']['templateFolder'])

    # Run the web server with the specified configuration
    logger.info(f'Starting web server at {config["flask"]["host"]}:{config["flask"]["port"]}')
    app.run(debug=False, host=config['flask']['host'], port=config['flask']['port'], threaded=config['flask']['threadedServer'])
