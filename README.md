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
    A dynamic site made in Flask that is able to generate intelligent embeds without any limitations from almost any video on Discord.
</p>

<br>

#### Features

- The website generates a video player with the direct video url you provide in the Discord preview. It's useful for people who don't have Nitro and want to send very large videos to other people quickly and easily.

#### How to use

Basically, the site has a main base url and 4 parameters, 1 of which is required. The parameters are used to generate the embed with the video player and the thumbnail image you want to use (warning: the site will only send a valid response to the bot that Discord uses to display the player to the end user).

- Base API URL: https://discoembed.onrender.com.

Parameters:

- **`url`** (required): the direct video url you want to generate the embed _(H265/HEVC encoded videos or MKV files are not supported)_.
- **`cover`** (optional): the thumbnail image you want to use in the embed _(It must be a direct image url)_.
- **`width`** (optional): the width of the video player _(Default is 1920)_.
- **`height`** (optional): the height of the video player _(Default is 1080)_.

#### How was it done?

- Built with [Python](https://www.python.org).
- Uses [Flask](https://flask.palletsprojects.com) as the web framework.

#### Prerequisites

- [Python 3.12.4](https://www.python.org/downloads/release/python-3124) with pip.
- [Git](https://gitforwindows.org) (optional).
- Any browser that supports HTML5, CSS3 and JavaScript.

### Installation from source code

```bash
# 1. Clone the repository
git clone https://github.com/henrique-coder/discoembed.git

# 2. Change the directory
cd discoembed

# 3. Install the requirements
pip install -U -r requirements.txt

# 4. Run the web server
python discoembed.py  # with Python (development)
gunicorn -b 0.0.0.0:18500 discoembed:app  # with Gunicorn (production)
```

### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have any suggestions that could improve this project, please [fork](https://github.com/henrique-coder/discoembed/fork) the repository and open a pull request. Or simply open an [issue](https://github.com/henrique-coder/discoembed/issues/new) and describe your ideas or let us know what bugs you've found. Don't forget to give the project a star. Thanks again!

1. Fork the project at https://github.com/henrique-coder/discoembed/fork
2. Create your feature branch ・ `git checkout -b feature/{feature_name}`
3. Commit your changes ・ `git commit -m "{commit_message}"`
4. Push to the branch ・ `git push origin feature/{feature_name}`
5. Open a pull request describing the changes made and detailing the new feature. Then wait for an administrator to review it and you're done!

### License

Distributed under the **MIT License**. See [LICENSE](https://github.com/henrique-coder/discoembed/blob/main/LICENSE) for more information.

### Disclaimer

Please note that this project is still under development and may contain errors or incomplete functionality. If you encounter any problems, feel free to open an [issue](https://github.com/henrique-coder/discoembed/issues/new) and describe the problem you are facing. Your feedback is very important to us.