<h2 align="center">Discoembed</h2>

<p align="center">
    <img src="icon.ico" alt="favicon" width="64" height="64">
</p>

<br>

<p align="center">
    <img src="https://img.shields.io/github/created-at/henrique-coder/discoembed?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub Created At">
    <img src="https://img.shields.io/github/commit-activity/m/henrique-coder/discoembed?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub commit activity">
    <img src="https://img.shields.io/github/last-commit/henrique-coder/discoembed?style=for-the-badge&logoColor=white&labelColor=gray&color=white" alt="GitHub last commit">
</p>

<p align="center">
    A dynamic service that generates smart Discord video embeds without limitations for almost any video.
</p>

<br>

## Features

- Generates a video player embed with any direct video URL for Discord preview
- Useful for users without Nitro who want to share large videos easily
- Supports custom cover images, video dimensions, and automatic URL validation
- Responds only to the Discord bot user agent for embed rendering

## API Usage

**Base URL:** `https://discoembed.henriquecoder.com/v1`

### `GET /`

Generates an HTML page with Open Graph and Twitter Card meta tags for Discord video embedding.

| Parameter | Type     | Required | Default | Description                                          |
| --------- | -------- | -------- | ------- | ---------------------------------------------------- |
| `url`     | `string` | Yes      | —       | Direct video URL _(H265/HEVC and MKV not supported)_ |
| `cover`   | `string` | No       | —       | Direct URL of the thumbnail/cover image              |
| `width`   | `int`    | No       | `1920`  | Width of the video player in pixels                  |
| `height`  | `int`    | No       | `1080`  | Height of the video player in pixels                 |

### `GET /status`

Returns the API health status.

```json
{
  "status": "ok",
  "service": "Discoembed"
}
```

## Tech Stack

- [Python](https://www.python.org) `>=3.10,<3.15`
- [FastAPI](https://fastapi.tiangolo.com) — Web framework
- [curl-cffi](https://github.com/lexiforest/curl-cffi) — HTTP client with TLS fingerprint support
- [Pydantic](https://docs.pydantic.dev) — Data validation and settings
- [Loguru](https://github.com/Delgan/loguru) — Logging
- [UV](https://docs.astral.sh/uv/) — Package manager

## Prerequisites

- [Python](https://www.python.org) `>=3.10`
- [UV](https://docs.astral.sh/uv/) (or install via `pip install uv`)
- [Just](https://github.com/casey/just) _(optional, for task running)_

## Installation

```bash
# Clone the repository
git clone https://github.com/henrique-coder/discoembed.git
cd discoembed

# Install dependencies
uv sync

# Run the development server
just dev
# Or without just:
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 18500
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have any suggestions that could improve this project, please [fork](https://github.com/henrique-coder/discoembed/fork) the repository and open a pull request. Or simply open an [issue](https://github.com/henrique-coder/discoembed/issues/new) and describe your ideas or let us know what bugs you've found. Don't forget to give the project a star!

1. Fork the project at https://github.com/henrique-coder/discoembed/fork
2. Create your feature branch — `git checkout -b feature/{feature_name}`
3. Commit your changes — `git commit -m "{commit_message}"`
4. Push to the branch — `git push origin feature/{feature_name}`
5. Open a pull request

## License

Distributed under the **MIT License**. See [LICENSE](https://github.com/henrique-coder/discoembed/blob/main/LICENSE) for more information.
