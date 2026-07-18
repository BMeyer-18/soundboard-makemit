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

- A [Rapberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) model or higher with its official power supply or adequate replacement. And in order to work with the libraries in this project, you will need to install a 64-bit OS like [Raspberry Pi's current 64-bit OS](https://www.raspberrypi.com/software/operating-systems/).

- A [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-3/) or better.

- Since the Raspberry Pi 3 comes with a headphone jack socket, you can use almost any functional speaker that meets your needs.

- 3D printable files will also be included for you to use in this repo to build a housing for the device.

### Pi Requirements

For this project, the Raspberry Pi only requires the files that allow you to use the model, so, after training the model, you can copy the following files to a new folder to then put onto a Pi along with this README: ```pi-requirements.txt, seeing_soundboard_main.py, play_audio.py, gesture_classification.py, gesture_recognizer.task```. You can also copy the entire project repository to save time with reconfiguring the files. That's up to you, but you shouldn't need any of the other files to run this.

### Testing the Application

Before we make the soundboard, we'll need to configurate a  couple of things manually on the Pi first.
