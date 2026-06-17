# Hand Gesture Soundboard  

## Overview

This was a project for the 2025 MakeMIT Hackathon that converts hand gestures into sounds. This code allows you to train and use your own model, as long as you have a dataset of images to train the model on. This uses MediaPipe Model Maker, which requires some outdated versions of Python libraries all listed in `requirements.txt`.  

## Data Setup  

To train the model, Mediapipe Model Maker requires you to set up your training directory in a specific way. You don't need to create a test/train/val split - that's done for you. All you need to do is create one folder for each of your hand gesture categories, and fill each folder with pictures of that hand gesture in use. You can include as few or as many as you want, but your data directory must only contain folders, each of which contains images of a specific hand gesture.

**Example data directory setup:**

    ├── dataset/
      ├── gesture_name_1/
        ├── img1.jpg
        ├── img2.jpg
      ├── gesture_name_2/
        ├── img1.png
        ├── img2.png

> Note that images used for training can only be in the .jpg or .png format.

To change the sounds that play, you'll need to change some code in `play_audio.py`. The detailed instructions along with a functional example can all be found there, but as a brief overview: You'll need to pair the name of each hand gesture with the directory of the corresponding sound effect, as well as its approximate length in seconds.

## Commands  

The argparser Python library is used to allow all your work training and using the model to be done in the terminal, with the exception of changing the sounds in `play_audio.py`. This has only been tested on Ubuntu so far.  
The following are the two commands you should need to use. All text in [square brackets] will need to be replaced with a directory.  
  
To train the model, use this command:
```python seeing_soundboard_main.py --train --data-path [data directory] --model-path [directory where trained model will be saved]``` **OR** ```python seeing_soundboard_main.py -t -d [data directory] -m [model directory]```

To use your trained model, use this command:  
```python seeing_soundboard_main.py --use --model-path [path to trained model, which should be a .task file]``` **OR** ```python seeing_soundboard_main.py --use -m [model path]```
