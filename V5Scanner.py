'''
This program handles the text processing for
the automatic barcode scanner

Version: 5
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

logNumber = int(input("Enter Log Number: ")) # Global variable for the hard drive log number
driveNum = 1 # define global variable for drive number
hardDriveList = ["hard_drive_1.jpg", "hard_drive_2.jpg","hard_drive_3.jpg","hard_drive_4.jpg","hard_drive_5.jpg","hard_drive_6.jpg","hard_drive_7.jpg","hard_drive_8.jpg","hard_drive_9.jpg","hard_drive_10.jpg","hard_drive_11.jpg","hard_drive_12.jpg","hard_drive_13.jpg","hard_drive_14.jpg","hard_drive_15.jpg","hard_drive_16.jpg","hard_drive_17.jpg","hard_drive_18.jpg","hard_drive_19.jpg","hard_drive_20.jpg"]
HDIndex = 0
barcodeMastList = [] # Master list with detected barcodes
snMasterList = [] # Master list with all text based serial numbers
manuMasterList = [] # Master list with all manufacturers
manufacturerList = ["hp", "intel", "hgst", "dell", "seagate", "toshiba", "wd"] # List of common manufacturers

hardDriveIndex = 0 # must be global otherwise resets to 0 every time, which is bad!

def manufacturers(): # Add more manufacturers
    global manufacturerList
    print("These are the current manufacturers: " + str(manufacturerList))
    add = input("Would you like to add more manufacturers? (Y/N): ")
    while add.upper() != "Y" or add.upper() != "N":
        if add.upper() == "Y":
            newManu = (input("Please enter one additional manufacturer: ")).lower()
            manufacturerList.append(newManu)
            add = input("Would you like to add more manufacturers? (Y/N): ")
        elif add.upper() == "N":
            break
        else:
            print("Please type a valid answer")
            add = input("Would you like to add more manufacturers? (Y/N): ")


# Initialize the camera for first image processing and take picture
def takePicture():
    global hardDriveList
    global HDIndex
    for i in range(20):
        time.sleep(1)
        picam2.capture_file("Hard_Drive_Pics_" + str(logNumber) + "/" + hardDriveList[HDIndex]) # Saves images to dedicated image directory for each hard drive log
        print("Image " + str(i+1) + " captured")
        time.sleep(5) # this will be replaced with the stepper mover function
        HDIndex = HDIndex + 1  
    if HDIndex >= 19: # Resets after each set of 20
        HDIndex = 0

# Compiles all barcodes into a list and then fills in boundaries with white pixels
def barcodeDetector():
    print("yee")


# Tokenization test - inspired by https://github.com/cherry247/OCR-bill-detection/blob/master/ocr.ipynb
# This method is less convoluted than the one above, and way simpler, but I must test it first
def textProcessor():
    global serialNumber # makes serialNumber global so other functions can access it
    serialNumber = ""
    global manufacturer 
    manufacturer = ""
    global hardDriveIndex
    
    hdImage = "/home/bobcaticus/barcodeScanner/Hard_Drive_Pics_" + str(logNumber) + "/" + hardDriveList[hardDriveIndex] # Goes through global hard drive jpg list
    # hdImage = cv2.cvtColor(hdImage, cv2.COLOR_BGR2GRAY) # Convert to greyscale for better processing - not working right now
    hardDriveIndex = hardDriveIndex + 1 # Prepares for next loop
    
    rawText = pytesseract.image_to_data(hdImage, output_type=Output.DICT) # Raw dictionary 
    recordedList = rawText['text'] #Text list subset of rawText diciontary
    recordedString = ' '.join(rawText['text'])

    #Tokenization time and string/list splicing
    print("RAW LIST: \n")
    print(recordedList)

    noPunctuation = nltk.RegexpTokenizer(r"\w+")
    noPunctuationWordList = noPunctuation.tokenize(recordedString) # Edited list with no punctuation
    print("TOKENIZED W/PUNCTS REMOVED \n")
    print(noPunctuationWordList)

    serial_combos = ["sn", "isn", "s/n", "sin"]
    for indices in range(len(noPunctuationWordList)): # goes through noPunctuationWordList to search for terms
        for x in range(len(manufacturerList)):
            if (noPunctuationWordList[indices]).lower() == manufacturerList[x]: # For loop that searches for manufacturer
                manufacturer = noPunctuationWordList[indices]
                print("Manufacturer found: " + manufacturer)
        
        # Searches for serial num case if the letters "s" and "n" are seperated
        if indices <= (len(noPunctuationWordList) - 2): # Avoid index out of range errors
            if (noPunctuationWordList[indices][0]).lower() == "s" and (noPunctuationWordList[indices+1][0]).lower() == "n": 
                barcodeIndex = indices + 2
                serialNumber = noPunctuationWordList[barcodeIndex] 
                print("Serial number found: " + serialNumber)

        # Searches for serial_combos if they are together
        if indices <= (len(noPunctuationWordList) - 1): # Avoid index out of range errors
            for y in range(len(serial_combos)):
                if (noPunctuationWordList[indices]).lower() == serial_combos[y]: # sorts through the words in the text dictionary and compares them with the possible serial number key
                    barcodeIndex = indices + 1
                    serialNumber = noPunctuationWordList[barcodeIndex] 
                    print("Serial number found: " + serialNumber) # Prints indicator combos


    # Redundancies if computer vision does not detect anything
    if serialNumber == "":
        serialNumber = "not found"
    if manufacturer == "":
        manufacturer = "not found" # !!! ADD another computer vision passthrough that just detects the hard drive manufacturer
    
    snMasterList.append(serialNumber) # Adds SN to master list
    manuMasterList.append(manufacturer) # Adds manufacturer to a master list   

# Final check to make sure everything is input correctly
def verify():
    for i in range(20):  
        print("\n| HDD Num: " + str(i+1) + "| HDD Manufacturer: " + manuMasterList[i] + "| HDD Serial Number: " + snMasterList[i] + "|")
    verifyConf = input("Would you like to change any manufacturers or serial numbers? (Y/N): ")
    while verifyConf.upper() != "Y" or verifyConf.upper() != "N":
        if verifyConf.upper() == "Y":
            hddNum = input("Please enter the number of the drive you want to change: ")
            snValidation = input("Is the serial number correct? (type Y/N): ")
            while snValidation.upper() != "Y" or snValidation.upper() != "N": # Ensures user enters valid answer - redundancy
                if snValidation.upper() == "Y":
                    break
                elif snValidation.upper() == "N":
                    snMasterList[int(hddNum) - 1] = input("Type or scan in the correct serial number please: ")
                    break
                else:
                    print("Please type a valid answer")
                    snValidation = input("Is the serial number correct? (Y/N): ")

            manuValidation = input("Is the manufacturer correct? (type Y/N): ")
            while manuValidation.upper() != "Y" or manuValidation.upper() != "N": # Ensures user enters valid answer - redundancy
                if manuValidation.upper() == "Y":
                    break
                elif manuValidation.upper() == "N":
                    manufacturer = input("Type in the correct manufacturer: ")
                    manufacturerList[int(hddNum) - 1] = manufacturer
                    break
                else:
                    print("Please type a valid answer")
                    manuValidation = input("Is the manufacturer correct? (Y/N): ")
            verifyConf = input("Would you like to change any additional manufacturers or serial numbers? (Y/N): ")   

        elif verifyConf.upper() == "N":
            break

        else:
            print("Please type a valid answer")
            verifyConf = input("Would you like to change any manufacturers or serial numbers? (Y/N): ")


#Function that writes the HDD report
def writeReport():
    global logNumber
    os.system("mkdir Hard_Drive_Pics_" + str(logNumber))
    #takePicture()
    for i in range(20):
        textProcessor()
    verify()
    csvScribe()
    print("Report #" + str(logNumber) + " completed")
    time.sleep(3)
    logNumber = int(logNumber) + 1 # Update logNumber so a new table is made each time

# Might be redundanct (cvsCreator already does the job)
def header():
    # /home/pi/barcodeScanner/Hard_Drive_Log_'
    with open(('/home/bobcaticus/barcodeScanner/Hard_Drive_Log_' + str(logNumber) + '.csv'), 'a', newline='') as driveLog:  
        header = ['Number', 'Manufacturer', 'Hard Drive Serial Number'] # Column data
        # Pass the CSV  file object to the writer() function
        writer_object = writer(driveLog)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(header)  
        # Close the file object
        driveLog.close()
    
def csvScribe():
    with open(('/home/bobcaticus/barcodeScanner/Hard_Drive_Log_' + str(logNumber) + '.csv'), 'a', newline='') as driveLog:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(driveLog)
        for x in range(20):
            driveData = [x+1, manuMasterList[x], snMasterList[x]] # Column data from master list
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(driveData)  
        # Close the file object
        driveLog.close()

# This is the master function, which controls all the processes and has
# the direct override to kill the program

def looper():
    header()
    writeReport()

    writeAnother = input("Would you like to complete another report? (Y/N): ")
    while writeAnother.upper() != "Y" or writeAnother.upper() != "N": # Ensures user enters valid answer - redundancy
        if writeAnother.upper() == "Y":
            looper()
        elif writeAnother.upper() == "N":
            print("Goodbye: ")
            sys.exit()
        else:
            print("Please type a valid answer")
            writeAnother = input("Would you like to complete another report? (Y/N): ")

# Functions called here to execute the program
manufacturers() # Add additional manufacturers
looper()







