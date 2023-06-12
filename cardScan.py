'''
This program handles the text processing for
the automatic card scanner

Version: 1
Author: Lamine Sao
'''
from picamera2 import Picamera2, Preview
from platform import python_branch
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import nltk 
from nltk.tokenize import word_tokenize
import time # for taking camera stills
import keyboard
import mysql.connector
from csv import writer
import os
from PIL import Image
import sys

# Set camera parameters 
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (3280, 2464)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()

picSet = int(input("Enter picture set number: ")) # Global variable for the hard drive log number
cardPicList = []
cardList = []
cardIndex = 0 # must be global otherwise resets to 0 every time, which is bad!
imagesTaken = 0

for i in range(30):
    cardPicList.append("card_" + str((i + 1)) + ".jpg")


# Initialize the camera for first image processing and take picture
def takePicture():
    global cardPicList
    global imagesTaken
    for i in range(30):
        take = input("Take a photo (y/n): ")
        if (take.lower() != "n"):
            imagesTaken = imagesTaken + 1
            picam2.capture_file("Card_Pics_" + str(picSet) + "/" + cardPicList[i]) # Saves images to dedicated image directory for each hard drive log
            print("Image " + str(i+1) + " captured")


# Tokenization test - inspired by https://github.com/cherry247/OCR-bill-detection/blob/master/ocr.ipynb
# This method is less convoluted than the one above, and way simpler, but I must test it first

def textImageProcessor():
    global cardIndex

    hdImage = "/home/bobcaticus/cardScanner/Card_Pics_" + str(picSet) + "/" + cardPicList[cardIndex] # Goes through global hard drive jpg list
    croppedImage = Image.open(hdImage)
    # Setting the points for cropped image
    left = 1700
    top = 330
    right = 2660
    bottom = 475
    
    # Cropped image of above dimension
    # (It will not change original image)
    croppedImage = croppedImage.crop((left, top, right, bottom))

    # hdImage = cv2.cvtColor(hdImage, cv2.COLOR_BGR2GRAY) # Convert to greyscale for better processing - not working right now
    cardIndex = cardIndex + 1 # Prepares for next loop
    rawText = pytesseract.image_to_data(croppedImage, output_type=Output.DICT) # Raw dictionary 
    recordedList = rawText['text'] #Text list subset of rawText diciontary
    recordedString = ' '.join(rawText['text'])
    print("Recorded String \n" + recordedString)
    cardList.append(recordedString)

def fixCardDataAndAdd():
    for i in range(30):
        print("Recorded Card Serial Numbers: \n")
        print("Card #" + str(i+1) + ": " + cardList[i] + "\n")

    needToFix = (input("Do you want to manually fix serial numbers? (Y/N)"))
    while needToFix.upper() != "Y" or needToFix.upper() != "N":
        if needToFix.upper() == "Y": # NEED TO  ADD INCORRECT INPUT REJECTION ie. non integer inputs, 0 entered by accident
            cardNumToFix = int(input("Enter the number you want to fix (ie. 1, 3, 20): "))
            print("You have chosen to fix card #" + str(cardNumToFix) + ": " + cardList[cardNumToFix - 1])
            correctNum = input("Enter the corrected serial number: ")
            cardList[cardNumToFix - 1] = correctNum
        elif needToFix.upper() == "N":
            break
        else:
            print("Please type a valid answer")
        needToFix = (input("Do you want to manually fix serial numbers? (Y/N)"))

#Function that writes the HDD report
def writeReport():
    global picSet
    global cardList
    processFromExisting = input("Would you like to input from an existing folder? (Y/N): ")

    if processFromExisting.upper() == "Y":
        picSet = int(input("Enter picture set number: "))
        for i in range(30):
            textImageProcessor()
    else:
        os.system("mkdir Card_Pics_" + str(picSet))
        takePicture()
        for i in range(30):
            textImageProcessor()
    fixCardDataAndAdd()
    csvScribe()
    print("Report #" + str(picSet) + " completed")
    time.sleep(3)

# Might be redundanct (cvsCreator already does the job)
def header():
    # /home/pi/barcodeScanner/Hard_Drive_Log_'
    with open(('/home/bobcaticus/cardScanner/Card_Log_1.csv'), 'a', newline='') as driveLog:  
        header = ['Serial_Number'] # Column data
        # Pass the CSV  file object to the writer() function
        writer_object = writer(driveLog)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(header)  
        # Close the file object
        driveLog.close()
    
def csvScribe():
    with open(('/home/bobcaticus/cardScanner/Card_Log_1.csv'), 'a', newline='') as driveLog:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(driveLog)
        for x in range(30):
            driveData = [cardList[x]] # Column data from master list
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(driveData)  
        # Close the file object
        driveLog.close()

# This is the master function, which controls all the processes and has
# the direct override to kill the program

def looper():
    global picSet
    global cardIndex
    global imagesTaken
    header()
    writeReport()

    writeAnother = input("Would you like to complete another report? (Y/N): ")
    while writeAnother.upper() != "Y" or writeAnother.upper() != "N": # Ensures user enters valid answer - redundancy
        if writeAnother.upper() == "Y":
            picSet = int(input("Enter picture set number: "))
            cardIndex = 0
            imagesTaken = 0
            looper()
        elif writeAnother.upper() == "N":
            print("Goodbye: ")
            sys.exit()
        else:
            print("Please type a valid answer")
            writeAnother = input("Would you like to complete another report? (Y/N): ")

# Functions called here to execute the program
looper()







