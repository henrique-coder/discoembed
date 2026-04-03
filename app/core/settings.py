from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Discoembed"
    base_url: str = "https://discoembed.henriquecoder.com"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 18500

    csp_default_src: str = "'self' https://cdnjs.cloudflare.com"
    csp_style_src: str = "'self' 'unsafe-inline' https://cdnjs.cloudflare.com"
    csp_script_src: str = "'self' https://cdnjs.cloudflare.com"

    allowed_origins: list[str] = Field(
        default=[
            "https://discoembed.henriquecoder.com",
            "https://discoembed.vercel.app",
        ]
    )

    discord_bot_user_agent: str = "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"

    default_video_url: str = "https://i.imgur.com/k9FrlEe.mp4"
    default_cover_url: str = "https://i.imgur.com/bUNtIgQ.png"
    invalid_url_video_url: str = "https://i.imgur.com/bMGv6H5.mp4"
    invalid_url_cover_url: str = "https://i.imgur.com/kTj9dnk.png"
    invalid_cover_url: str = "https://i.imgur.com/Cl6kMsz.png"
    missing_cover_url: str = "https://i.imgur.com/8ZkUMGK.png"
    default_width: int = 1920
    default_height: int = 1080

    base_dir: Path = Path(__file__).resolve().parent.parent
    template_dir: Path = Path(__file__).resolve().parent.parent / "templates"

    model_config = {
        "env_prefix": "DISCOEMBED_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
