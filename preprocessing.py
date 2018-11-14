"""
Rename ill-formatted files, reorient files.
Version of the 20180924.
"""

import os
from PIL import Image
import piexif
import datetime

def rotate_jpeg(filename):
    """
    Rotate and remove 'Orientation' of exif value (https://stackoverflow.com/questions/47869107/)

    Input:
    -filename       string
    """

    img = Image.open(filename)
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

            img.save(filename, exif=exif_bytes)

def rename_file_with_colons(file):
    """
    Rename a file for which the date contains colons.

    Input:
    -file       string
    """

    new_file_name = file.split(" ")

    date_as_list = new_file_name[0].split(":")

    for i, element in enumerate(date_as_list):

        if len(element) < 2:

            date_as_list[i] = "0" + element

    new_file_name = "".join(date_as_list) + "_" + new_file_name[1]

    os.rename(
        folder_name + "/" + file,
        folder_name + "/"  + new_file_name
    )

def rename_file_with_dashes(file):
    """
    Rename a file for which the date contains dashes.

    Input:
    -file       string
    """

    new_file_name = file.split(" ")

    date_as_list = new_file_name[0].split("-")

    for i, element in enumerate(date_as_list):

        if len(element) < 2:

            date_as_list[i] = "0" + element

    new_file_name = "".join(date_as_list) + "_" + new_file_name[1]

    os.rename(
        folder_name + "/" + file,
        folder_name + "/"  + new_file_name
    )

def rename_file_with_periods(file):
    """
    Rename a file for which the date contains periods.

    Input:
    -file       string
    """

    new_file_name = "".join(file.split(".")[:-1]) + "." + file.split(".")[-1]

    os.rename(
        folder_name + "/" + file,
        folder_name + "/"  + new_file_name
    )

folder_name = "/Volumes/3TO_TIBO/Photos/2013/portable"

for file in os.listdir(folder_name):

    if ":" in file:

        rename_file_with_colons(file)

for file in os.listdir(folder_name):

    if " " in file:

        rename_file_with_dashes(file)

for file in os.listdir(folder_name):

    if len(file.split(".")) > 2:

        rename_file_with_periods(file)

for file in os.listdir(folder_name):

    if file.startswith("2"):

        if not file.endswith((
            ".mov",
            ".MOV",
            ".mp4",
            ".MP4",
            ".gif",
            ".GIF",
            ".3gp",
            ".3GP",
        )):

            print(file)

            rotate_jpeg(folder_name + "/"  + file)
