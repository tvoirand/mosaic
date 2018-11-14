"""
To test if the exif of a file is corrupted.
Version of the 20180921.
"""

from PIL import Image
import piexif
import argparse

parser = argparse.ArgumentParser("Test if image exif corrupted.")
parser.add_argument("-f", help="input file")
args = parser.parse_args()


file = args.f

img = Image.open(file)

if "exif" in img.info:

    print("there is an exif")

    exif_dict = piexif.load(img.info["exif"])
    exif_bytes = piexif.dump(exif_dict)
