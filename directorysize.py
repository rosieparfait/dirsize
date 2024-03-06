from genericpath import getsize
from decimal import *
import os
import collections

getcontext().prec = 28


def format_bytes(bytes): # Formats raw byte number to shorten it.
    formatted = Decimal(bytes)
    order = 0

    prefixes = ['', 'K', 'M', 'G', 'T']

    while formatted >= 1024:
        formatted /= 1024
        order += 1

    return str(round(formatted, 1)) + " " + prefixes[order] + "B"

def folder_size(folder, order = 0):
    totalbytes = 0

    folders = {}

    try:
        for element in os.scandir(folder):
            if element.is_file():
                totalbytes += os.path.getsize(element.path)

                # print("found file " + element.name)

            elif element.is_dir() and not element.is_symlink() and element.name != "OneDrive" and element.name != "dosdevices" and element.name != "crossover": # On Windows, OneDrive can still be accessed thru the User folder, let's ignore this :) also included a dosdevices and crossover thing cus if you have wine on mac it enters a loop
                subsize = folder_size(element.path, order + 1) # Recursion! Might have to worry about stack size?
                totalbytes += subsize                

                if order == 0:
                    print(element.name + "... " + format_bytes(subsize)) # Lists all direct subfolders of folder of interest.

                    folders[subsize] = element.name

    except NotADirectoryError:
        return os.path.getsize(folder)

    except:
        return 0;

    if order == 0:
        print("\n\n")

        ordered_folders = collections.OrderedDict(sorted(folders.items()))

        for k, v in ordered_folders.items():
            print(v + "... " + str(format_bytes(k)))

    return totalbytes

folderpath = input("Please input folder path below: \n")

print("\n\nTotal Size: " + format_bytes(folder_size(folderpath)))
