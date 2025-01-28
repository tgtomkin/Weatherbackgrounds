# All functions that interact with the settings file will be placed in this file.
from Weatherbackgrounds import build_timestamp

# print out passed-in settings values
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