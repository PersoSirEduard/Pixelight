# Pixelight
An easy way to convert images and videos to pixel art for game devs who hate making pixel art assets.

## Overview
Pixelight is a personal Python CLI project created in order to generate pixel art assets quickly and efficiently. It can handle both images and videos without any headaches.

Input | Output
------|------
![Street](https://i.imgur.com/edlx4nll.jpeg) | ![Pixelated street](https://i.imgur.com/OY0yImUl.png)
![Bike](https://i.imgur.com/udwcUMwm.jpg) |  ![Pixelated bike](https://i.imgur.com/38OxI1em.png)
[![Dog](https://i.imgur.com/80fimlKm.mp4)](https://i.imgur.com/80fimlK.mp4) |  ![Pixelated dog](https://i.imgur.com/jFz3hvhm.gif)

## Installation

1) Clone the repository: `git clone https://github.com/PersoSirEduard/Pixelight.git`
2) Install requirements: `python -m pip install -r requirements.txt`
3) Done.

## Usage

```
usage: main.py [-h] [-v] [-s pixelation] [-p palette] [-c colors_count] [-o output] [-f framerate] file

positional arguments:
  file             Source file (*.png, *.jpg, *.jfif, *.bmp, *.mp4, *.avi, *.mov, *.gif)

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  -s pixelation    Pixelation factor (default is 10)
  -p palette       Palette (default is None) (default, auto, auto2, colorful, grey)
  -c colors_count  Colors counts (default is 10)
  -o output        Output file
  -f framerate     Output framerate (default is 10)
```
