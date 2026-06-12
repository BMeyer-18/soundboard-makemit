# MakeMIT-Visual-Soundboard #

## Table of Contents ##

1. Introduction

2. Hardware and Materials

3. Installation

4. Training the model

5. Trying it out on your computer

6. RasberryPi Intergration

7. Housing

---

### Introduction ###

This project started out as a submittion to the 2025 MakeMIT hardware hackthon from five college students: Arwen "Pippin" Fleet, Benjamin "Ben" Meyer, Christ-Ismael Kone, Rosalind Chang, and Thanadetch “Detch” Mateedunsatits.

We intended to build a "Visual/Seeing Soundboard," or a gesture recognizing piece of hardware that, when turned on, would use its camera to detect and identify hand gestures to play a specific sound based on that gesture. Conceptually, this device could be used for communication with those who have difficulty with oral communication or simply for entertaining purposes.

Although we weren't able to get it fully set up by the end of the hackthon, we ended up with such a solid proof of concept that some of us decided to finish the project. This repository should include the neccesary files and instructions needed to build this device.

---

### Hardware and Materials ###

The final build was completed using the following:

- [Rapberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/): This single-board computer acted as the host of the main programs' insterface. Later raspberry pi models from the 4th and 5th generations and beyond should also have no problem running these files with improved performance.

- [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/): This camera was chosen to act as the eye of the main board. However, any camera module compatible with a raspberry pi or intergrated using other microcontrollers should work as well.

- Speaker Module (Working on it)

- A 3D printer of your choice: The housing for this device can be created in any way you want, but the files provided for the housing in this repository were meant to be 3D printed.

- A PC or laptop with the following requirements: The latest version of Windows 11 or MacOS, Ubuntu 24.04 or later, or anyother linux distros able to create a virtual environment to install the nessecary packages require to train the model.

---

### Installation ###
