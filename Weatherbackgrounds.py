# TODO: minimize to system tray? idk if i care lol

import time
import requests
import schedule
import os
from tkinter import filedialog
# pics_url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/latest.jpg"

# create timestamp text for messages
def build_timestamp():
    time_val = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    time_string = "[" + time_val + "] - "
    return time_string

# print out settings values of pas
def print_settings(settings):
    print("URL: " + settings[0])
    print("Folder: " + settings[1])
    print("Time between downloads: " + settings[2])

# return generic settings list, print out values
def generic_settings():
    settings_list = ["https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/latest.jpg", "", "20"]
    print("Settings set to generic values:")
    print_settings(settings_list)
    return settings_list

# pull settings.txt file in same folder as .exe to code
# reverts to generic values if the opening of the file fails
def open_settings_file():
    settings_list = []
    try:
        with open('settings.txt', mode = 'r', encoding= 'utf-8-sig') as settings_file:
            lines = settings_file.readlines()
    except IOError as e:
        print(build_timestamp() + "IO Error when reading settings file Error{0}: {1}".format(e.errno, e.strerror))
        settings_list = generic_settings()
        return settings_list
    except:
        print(build_timestamp() + "Reading settings file failed")
        settings_list = generic_settings()
        return settings_list

    for line in lines:  # each setting is at the second position in each line, pull each value to be used later
        line = line.split(",")
        line = [i.strip() for i in line]
        settings_list.append(line[1])
    return settings_list

# attempt to download picture from given URL
def download_pics(picture_url):
    try:
        img_data = requests.get(picture_url).content
    except:
        print(build_timestamp() + "download failed")
        img_data = 0 # sets to 0 to be ignored before the store is attempted
    return  img_data

# takes photo data and overwrites current pics at file_path
# creates two to have the photos properly update when picture updates for windows slideshow option
def store_pics(picture_data, file_path):
    file1 = os.path.join(file_path,'latest1.jpg')
    file2 = os.path.join(file_path,'latest2.jpg')
    any_errors = 0
    try:
        # attempt to write first picture to folder
        with open(file1, 'wb') as handle:
            handle.write(picture_data)
    except IOError as e:
        # write error codes to output
        print("Error occurred when storing latest1.jpg please ensure the file is not open")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        any_errors = 1
    except:
        # else, write generic error
        print("Unexpected Error occurred when storing latest1.jpg please ensure the file is not open")
        any_errors = 1
    # if the first write worked, attempt to write second picture with same errors on failure
    else:
        try:
            with open(file2,'wb') as handle2:
                handle2.write(picture_data)
        except IOError as e:
            print("Error occurred when storing latest2.jpg please ensure the file is not open")
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            any_errors = 1
        except:
            print("Unexpected Error occurred when storing latest2.jpg please ensure the file is not open")
            any_errors = 1
    return any_errors


def download_and_store_pic(file_location, pic_url):
    print(build_timestamp() + "starting download")
    pic_data = download_pics(pic_url)
    if pic_data != 0:
        print(build_timestamp() + "download worked")
        pic_storing_errors = store_pics(pic_data,file_location)
        if pic_storing_errors == 0:
            print(build_timestamp() + "hey it worked")


def get_pic_filepath():
    pic_filepath = ""
    while pic_filepath == "":
        pic_filepath = filedialog.askdirectory()
        if pic_filepath == "":
            print("No folder selected, pictures will be placed in the same folder as Weatherbackgrounds.exe")
            print("Are you sure? Please type y/n to confirm")
            user_input = input()
            if user_input in ["y", "n"]:
                if user_input == "n":
                    continue
                if user_input == "y":
                    break
            else:
                print("Please answer y/n")
    return pic_filepath


def main():
    # have user select filepath on first run
    previous_settings = open_settings_file()
    picture_url = previous_settings[0] # set URL to settings.txt URL
    minutes_per_run = previous_settings[2] # set minutes_per_run to settings.txt minutes

    # check if filepath setting is empty, and request user to select filepath and update settings file accordingly
    if previous_settings[1] == '':
        pic_filepath = get_pic_filepath()
        with open('settings.txt', mode= 'w', encoding= 'utf-8-sig') as settings_file:
            settings_file.write("url, " + picture_url + "\noutput folder, "+
                                pic_filepath + "\nminutes, " + minutes_per_run)
    # if filepath is not empty, use settings.txt filepath
    else:
        pic_filepath = previous_settings[1]

    # create schedule job to run with information from settings file and immediately run on startup
    schedule.every(int(minutes_per_run)).minutes.do(
        download_and_store_pic, file_location=pic_filepath, pic_url = picture_url)
    schedule.run_all()

    # check for new schedule every second
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()