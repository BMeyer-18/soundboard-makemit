# MakeMIT-Visual-Soundboard (In Progress)

## Overview

This was a project for the 2025 MakeMIT Hackathon that converts hand gestures into sounds. This code allows you to train and use your own model, as long as you have a dataset of images to train the model on. This uses MediaPipe Model Maker, which requires some outdated versions of Python libraries all listed in `requirements.txt`.

## Data Setup

> If you don't want to gather a dataset of your own, you can skip the data setup and follow along using the files in the 'model_files' folder to get started. The recognized hand gestures are thumbs up, thumbs down, fist, peace sign, ok sign, and the ASL 'I love you' sign.

To train the model, Mediapipe Model Maker requires you to set up your training directory in a specific way. You don't need to create a test/train/val split - that's done for you. All you need to do is create one folder for each of your hand gesture categories, and fill each folder with pictures of that hand gesture in use. You can include as few or as many as you want, but your data directory must only contain folders, each of which contains images of a specific hand gesture.

**Example data directory setup:**

    ├── dataset/
      ├── gesture_name_1/
        ├── img1.jpg
        ├── img2.jpg
      ├── gesture_name_2/
        ├── img1.png
        ├── img2.png

**Note that images used for training can only be in the .jpg or .png format**. Aim for at least 25-50 images per gesture. 100+ images per gesture will provide you with the best accuracy.

To change the sounds that play, you'll need to change some code in `play_audio.py`. The detailed instructions along with a functional example can all be found there, but as a brief overview: You'll need to pair the name of each hand gesture with the directory of the corresponding sound effect, as well as its approximate length in seconds.

### Commands

The argparser Python library is used to allow all your work training and using the model to be done in the terminal, with the exception of changing the sounds in `play_audio.py`. So far, this has been tested in Ubuntu.

The following are the two commands you should need to use. All text in [square brackets] will need to be replaced with a directory.

To train the model, use this command:
```python seeing_soundboard_main.py -t -d [data directory] -m [model directory]```

> If you decide to train your own model, make sure to delete all the files in the 'model' folder to avoid redundancy. [model directory] is the directory where trained model will be saved and where you will have access to the 'gesture_recognizer.task' file to test out your model.

To use your trained model, use this command:
```python seeing_soundboard_main.py -u -m training_files/model/gesture_recognizer.task (or wherever the .task file you created is)```

### Common Issues

While trying to install requirements.txt, you might run into issues regarding mediapipe and tensorflow as those packages are no longer supported and therefore not available in the latests versions of python. This means that you will need to train and use the model using a version of python before 3.12. Python 3.10 and Python 3.11 where both used during testing to install requirements.txt with minimal issues.

If you have a later version of python already installed on your computer, you can use a virtual environment to work on this project. We recommend using [Anaconda](https://www.anaconda.com/docs/getting-started/main) (if you don't already use it) to create the required venv because it already comes with recognized packages for certain versions of mediapipe and tensorflow.

Furthermore. You might still run into an error while trying to train or use the module where certain modules aren't included in the versions you downloaded:

- `ModuleNotFoundError: No module named 'pkg_resources'`
- `ModuleNotFoundError: No module named 'mediapipe.tasks.cc'`

'pkg_resources' is a part of the 'setuptools' package, but some versions of setuptools ship without pkg_resources. The most reliable solution to either upgrade setuptool with `pip install --upgrade setuptools` or to replace whichever version you're using with the following:

    pip uninstall setuptools -y
    pip install setuptools==69.5.1

For 'mediapipe.task.cc', try downgrading to an earlier version of mediapipe:

    pip uninstall mediapipe mediapipe-model-maker -y
    pip install mediapipe==0.10.11 mediapipe-model-maker==0.2.1.4

## Hardware Setup

This section will provide all the neccessary information to run the model on a Rasperry Pi.

### Parts List

The prototype can be completed with the following parts:

- A [Rapberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) model or higher with its **official power supply or adequate replacement**. And in order to work with the libraries in this project, you will need to install a 64-bit OS like [Raspberry Pi's current 64-bit OS](https://www.raspberrypi.com/software/operating-systems/).

- A [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-3/). The files that allow you to interact with the Raspberry Pi camera are compatible with this camera only. You could also connect the Raspberry Pi to a USB webcam instead, avoiding the need for the file `pi_camera_server.py`.

- Since the Raspberry Pi 3 comes with a headphone jack socket, you can use almost any functional speaker that meets your needs. Speakers that use the Pi's GPIO pinout may require an additional layer of intergration that may not be coverted in the scope of this project.

- 3D printable files will also be included for you to use in this repo to build a housing for the device.

### Pi Requirements

For this project, the Raspberry Pi only requires the files that allow you to use the model, so, after training the model, you can copy the following files to a new folder to then put onto a Pi along with this README: ```pi-requirements.txt, seeing_soundboard_main.py, play_audio.py, gesture_classification.py, pi_camera_server.py, gesture_recognizer.task```. You can also copy the entire project repository to save time with reconfiguring the files. That's up to you, but the next set of instructions will assume that you've cloned the repository to your Raspberry Pi.

### Testing the Application

Before we make the soundboard, we'll need to configurate a couple of things manually on the Pi first.

Assuming configurating your raspberrypi went smoothly, you will need to be able to use both system python (most likely python 3.13 or higher) and an older version of python (3.10 - 3.12) using some python version mmanagement process like pyenv.

First, locate the 'soundboard-makemit' repository and head inside. To download pyenv, run:

    curl https://pyenv.run | bash

Then add pyenv to your shell startup file (`~/.bashrc` on Raspberry Pi OS) so it's available in every terminal session:

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc

Raspberry Pi OS Bookworm ships with Python 3.13 as the system interpreter, and `mediapipe` does not support 3.13. So, use pyenv to install Python 3.11 alongside it:

    pyenv install 3.11.11
    cd ~/soundboard-makemit
    pyenv local 3.11.11

That last command creates a `.python-version` file scoped to this folder, so any time you `cd` into the repo, pyenv automatically switches to 3.11 without affecting the system Python used elsewhere on the Pi.

These two python versions are requirted because this project needs two things that can't coexist in one interpreter:

- **`mediapipe`** (for gesture recognition) which has to run under pyenv's 3.11.
- **`picamera2`/`libcamera`** (for reading frames off the Camera Module) are installed via `apt`, and their compiled C extensions are built specifically against the system's Python 3.13.

Because of this, one process can't do both jobs. The solution used here is to split the camera and the gesture recognition into two separate processes that talk over a **Unix domain socket**:

- `camera_server.py` runs under system Python 3.13, owns the `Picamera2()` object, and serves raw RGB frames over a socket at `/tmp/soundboard_camera.sock`.
- `gesture_classification.py` runs under pyenv's Python 3.11, connects to that socket as a client, and reconstructs each frame into a numpy array for MediaPipe to run inference on.

### Installing dependencies for each interpreter

Install the camera-facing packages system-wide, using `apt` rather than `pip` so you get versions already linked against the Pi's camera stack:

    sudo apt install libcap-dev
    
Then install the gesture-recognition dependencies inside the pyenv-managed 3.11 environment (make sure you're still inside the repo folder so pyenv has switched versions) using either commands:

    pip install -r pi-requirements.txt
    pip install mediapipe python-vlc opencv-python-headless numpy

> Don't use `sudo` when installing or running anything meant for the pyenv environment.

### Running the setup

With both environments installed, start the camera server first (this must run under system Python, so no pyenv activation needed):

    cd ~/soundboard-makemit
    pyenv local system
    python3 pi_camera_server.py

Then, in the second terminal,run the gesture classification process under pyenv's 3.11:

    cd ~/soundboard-makemit
    python seeing_soundboard_main.py -u -m training_files/model/gesture_recognizer.task

If everything is wired up correctly, you should see frames flowing from the camera server into the classification process, and MediaPipe should begin returning gesture predictions as you make hand gestures in front of the camera. Additionally, `gesture_classification.py` should now provide a 'debugging frame' showing you what the last image captured using `libcamera`. If you're using an OS with a physical desktop environment, you can see what image is being outputed by navigating to your /tmp folder and opening `debug_frame.jpg` for a 'live footage view' of the program running.

### Running automatically on boot using systemd
