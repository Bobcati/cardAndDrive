# cardAndDrive

This repository contains the programs needed to run the automatic card ID scanner and hard drive serial number scanner.

## Installation
You will need to install several packages on your raspberry pi. In the linux terminal on the raspberry pi, enter the following one by one:

```bash
sudo apt-get install python3-h5py
sudo apt-get install libatlas-base-dev
pip3 install -U numpy
pip3 install nltk
nltk.download('punkt')
pip3 install keyboard
pip3 install opencv-python
sudo apt install tesseract-ocr
pip3 install pytesseract
```
Then, you will need to make a 

## Usage
Simply run the cardScanner.py file in your raspberry pi terminal by typing:
```bash
python3 
```
