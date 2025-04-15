# Standard modules
from pathlib import Path


# Application settings
APP_NAME: str = "Discoembed"
DEBUG: bool = False
HOST: str = "0.0.0.0"
PORT: int = 18500

# Security headers
CSP_DEFAULT_SRC: str = "'self' https://cdnjs.cloudflare.com"
CSP_STYLE_SRC: str = "'self' 'unsafe-inline' https://cdnjs.cloudflare.com"
CSP_SCRIPT_SRC: str = "'self' https://cdnjs.cloudflare.com"

# CORS settings
ALLOWED_ORIGINS: list[str] = ["https://discoembed.vercel.app"]

# Base directory for templates
BASE_DIR: Path = Path(__file__).resolve().parent.parent
TEMPLATE_DIR: Path = BASE_DIR / "templates"

# Discord Bot User Agent (Publicly visible)
DISCORD_BOT_USER_AGENT: str = "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"

# Default values
DEFAULT_VIDEO_URL = "https://i.imgur.com/k9FrlEe.mp4"
DEFAULT_COVER_URL = "https://i.imgur.com/bUNtIgQ.png"
INVALID_URL_VIDEO_URL = "https://i.imgur.com/bMGv6H5.mp4"
INVALID_URL_COVER_URL = "https://i.imgur.com/kTj9dnk.png"
INVALID_COVER_URL = "https://i.imgur.com/Cl6kMsz.png"
MISSING_COVER_URL = "https://i.imgur.com/8ZkUMGK.png"
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
