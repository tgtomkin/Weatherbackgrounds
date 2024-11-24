# TODO: use the settings.txt file
# TODO: create .exe???  minimize and show in system icons area???? idk how any of that works lol

import time
import requests
import schedule
import os
from tkinter import filedialog

# pic_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/latest.jpg"

def open_settings_file():
    # pull settings file in relative path to code
    with open('settings.txt', mode = 'r', encoding= 'utf-8-sig') as settings_file:
        lines = settings_file.readlines()
    settings_list = []
    for line in lines:  # each setting is at the second position in each line, pull each value to be used later
        line = line.split(",")
        line = [i.strip() for i in line]
        settings_list.append(line[1])
    return settings_list

def download_pics(picture_url):
    try:
        img_data = requests.get(picture_url).content
    except:
        # print("download failed")
        img_data = 0 # sets to 0 to be ignored before the store is attempted
    return  img_data

def store_pics(picture_data, file_path):
    # takes photo data and overwrites current pics at file_path
    # creates two to have the photos properly update when picture updates for windows slideshow option
    file1 = os.path.join(file_path,'latest1.jpg')
    file2 = os.path.join(file_path,'latest2.jpg')
    with open(file1, 'wb') as handle:
        handle.write(picture_data)

    with open(file2,'wb') as handle2:
        handle2.write(picture_data)

def download_and_store_pic(file_location, pic_url):
    # print("starting download")
    pic_data = download_pics(pic_url)
    if pic_data != 0:
        # print("picture exists")
        store_pics(pic_data,file_location)
    # print("hey it worked")

def main():
    # have user select filepath on first run
    previous_settings = open_settings_file()
    picture_url = previous_settings[0] # set URL to settings.txt URL
    minutes_per_run = previous_settings[2] # set minutes_per_run to settings.txt minutes
    # check if filepath setting is empty, and request user to select filepath and update settings file accordingly
    if previous_settings[1] == '':
        pic_filepath = filedialog.askdirectory()
        with open('settings.txt', mode= 'w', encoding= 'utf-8-sig') as settings_file:
            settings_file.write("url, " + picture_url + "\noutput folder, " + pic_filepath + "\nminutes, " + minutes_per_run)
    # if filepath is not empty, use settings.txt filepath
    else:
        pic_filepath = previous_settings[1]

    # create schedule job to run with information from settings file and immediately run
    schedule.every(int(minutes_per_run)).minutes.do(download_and_store_pic, file_location=pic_filepath, pic_url = picture_url)
    schedule.run_all()
    while True: # wait for schedule and then sleep
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()