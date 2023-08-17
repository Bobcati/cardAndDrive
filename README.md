# cardAndDrive

This repository contains the programs needed to run the automatic card ID scanner and hard drive serial number scanner.

## Installation
You will need to install several packages on your raspberry pi. In the linux terminal on the raspberry pi, enter the following one by one:

```bash
sudo apt-get install python3-h5py
sudo apt-get install libatlas-base-dev
pip3 install keyboard
pip3 install opencv-python
sudo apt install tesseract-ocr
pip3 install pytesseract
sudo apt-get install netatalk
```
Then, you will need to make a cardScanner folder by typing in the linux terminal on the raspberry pi:
```bash
mkdir cardScanner
```
Then you will need to clone this github repository with the following command
```bash
git clone https://github.com/Bobcati/cardAndDrive.git
```

## MacOS Usage
Next you need to enable a server to connect to your laptop. On the raspberry pi terminal type;
```bash
sudo nano /etc/netatalk/afp.conf
```
Then you must edit the [Homes] section from:
<img width="581" alt="Screen Shot 2022-12-23 at 3 48 50 PM" src="https://user-images.githubusercontent.com/108192537/209362810-9e644afc-81ff-44b5-abfe-5d30fc08742e.png">

   ; [Homes]

   ; based regex = /xxxx

to:

   [Homes] (note no “;”)

   basedir = /home (note no “;”)
   <img width="575" alt="Screen Shot 2022-12-23 at 3 49 07 PM" src="https://user-images.githubusercontent.com/108192537/209362847-b76cecec-a5be-4a42-b757-e8855170db6f.png">

Then type CTRL-X and then CTRL-S to save your changes.
Then you must type on the pi
```bash
sudo systemctl restart netatalk
```

Next, connect to the server on your mac by pressing on finder, go, and connect to server:
<img width="650" alt="Screen Shot 2022-12-23 at 3 52 52 PM" src="https://user-images.githubusercontent.com/108192537/209363328-3826bf21-2af0-4afc-8844-0eff3f527b21.png">

On your raspberry pi, type in the terminal:
```bash
ifconfig
```
Your raspberry pi's IP address should be located after:
```bash
wlan0: flags=<234567890987654> mut 1200
   inet 192.168.123.123 
```
The ip address listed inet is your pi's IP address. Keep note of it

Back on your mac, add a new server by typing afp:// followed by your serial number.
<img width="481" alt="Screen Shot 2022-12-23 at 4 02 37 PM" src="https://user-images.githubusercontent.com/108192537/209364515-11689cf0-7ab4-463f-a7ed-219ba2323023.png">
You will then be prompted to put in user credentials. USE YOUR RASPBERRY PI'S USERNAME AND PASSWORD
<img width="848" alt="Screen Shot 2022-12-23 at 4 21 30 PM" src="https://user-images.githubusercontent.com/108192537/209366959-b6c958ec-24a2-42cf-bf5a-b5b12098c932.png">
Now you can access the folders and files in your raspberry pi and edit them like they are on your mac.

## Windows Usage
With windows, you can connect to the pi using WinSCP (Windows secure copy)
Install the free and open source WinSCP tool using the following instructions: https://winscp.net/eng/download.php
When you open WinSCP, you will be prompted by a login screen similar to that of the server in MacOS. In the hostname, type in the pi IP address (instructions above). Then type the username and password you set for the raspberry pi during installation. 
<img width="586" alt="Screen Shot 2023-06-16 at 8 52 14 AM" src="https://github.com/Bobcati/cardAndDrive/assets/108192537/83bf0c92-21ad-4028-a109-3ed03831c9d2">

## Usage
Simply run the cardScanner.py file in your raspberry pi terminal by typing:
```bash
python3 cardScanner.py
```
You will be prompted to input a folder number, card batch size, and home directory (your username is your home director). Make sure your folder number is a different from the image folders you have made previously.
Align the card under the camera and press any letter on the keyboard except for "n" and then the enter key to to take a picture.

The program will create a csv file with all of the card numbers that you can upload to your computer using a netatalk server. Connect to the raspberry pi using the steps listed above. You will be able to drag and drop the csv file with the serial numbers onto your desktop using WinSCP or the MacOS server. 
Watch the demo video below: 
