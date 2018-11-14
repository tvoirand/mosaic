from PIL import Image
import argparse
import os
import inspect
import sys
import random

def import_config(config_argument):
    """
    Create config dictionnary based on formatted config text files.
    Default config file must be name config_default.txt and be placed in same folder as python file.

    Input:
    -config_argument    None, or string
    """

    def read_config_file(config_file, config_dict):
        """
        Read config file and store parameters in dictionnary.

        Input:
        -config_file    string
        -config_dict    dictionnary
        """

        with open(config_file, "r") as file:

            file_contents = file.readlines()

        for line in file_contents:

            if not line.startswith("#"):

                param = line.split("=")[0].split()[0]

                value = line.split("=")[1].split()[0]

                config_dict[param] = value

        return config_dict

    if os.path.dirname(inspect.getfile(inspect.currentframe())) == "":
        config_default_file = "config_default.txt"
    else:
        config_default_file = os.path.dirname(inspect.getfile(inspect.currentframe())) \
            + "/config_default.txt"

    config = read_config_file(config_default_file, {})

    if config_argument != None:
        config = read_config_file(config_argument, config)

    return config

def check_image_file(file, width, height):
    """
    Checks if file is image of minimal size.

    Input:
    -file       string
    -width      integer
    -height     integer
    Output:
    -           boolean
    """

    if file.endswith((
        ".png",
        ".PNG",
        ".jpeg",
        ".JPEG",
        ".jpg",
        ".JPG",
        ".bmp"
    )):

        img = Image.open(file)

        if img.size[0] >= width and img.size[1] >= height:

            return True

        else:

            return False

    return False

def prompt_progress(iterations_done, iterations_total):

    progress_percent = iterations_done * 100.0 / iterations_total

    sys.stdout.write("Progress: {0:.2f} % \r".format(progress_percent))
    sys.stdout.flush()

def resize_input_image(image, width, height):
    """
    Resize input image.

    Input:
    -image      Image object
    -width      integer
    -height     integer
    """

    ratio = max(width / image.size[0], height / image.size[1])

    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))

    image = image.resize(new_size)

    left = (image.size[0] - width) // 2
    right = left + width
    top = (image.size[1] - height) // 2
    bottom = top + height

    image = image.crop((left, top, right, bottom))

    return image

def find_ratio(nb_of_values, target_ratio):
    """
    Finds the number of rows and columns which comes closest to a given ratio.

    Input:
    -nb_of_values   integer
    -target_ratio   float
    Output:
    -rows           integer
    -cols           integer
    """

    options = []

    cols = 1
    rows = nb_of_values

    while cols < rows:

        ratio = float(cols) / float(rows)

        options.append([rows, cols, ratio])

        cols += 1
        rows = nb_of_values // cols

    rows, cols, ratio = options[0][0], options[0][1], options[0][2]

    for option in options:

        if abs(target_ratio - option[2]) < abs(target_ratio - ratio):

            rows, cols, ratio = option[0], option[1], option[2]

    return rows, cols

def remove_random(input_list, elements_to_remove):
    """
    Removes a given number of elements from a list randomly.

    Input:
    -input_list             list
    -elements_to_remove     integer
    Output:
    -input_list             list
    """

    for step in range(elements_to_remove):

        random_index = random.randint(0, len(input_list))

        input_list.pop(random_index)

    return input_list

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Mosaic of images.")
    parser.add_argument("-config", help="custom configuration file")
    args = parser.parse_args()

    config = import_config(args.config)

    fragment_side = int(config["fragment_side"])
    input_min_width = int(config["input_min_width"])
    input_min_height = int(config["input_min_height"])

    files_list = os.listdir(config["input_directory"])
    files_list.sort()

    for file in files_list:

        if not check_image_file(
            config["input_directory"] + "/" + file,
            input_min_width,
            input_min_height
        ):

            files_list.remove(file)

    nb_of_images = len(files_list)

    rows, cols = find_ratio(nb_of_images, float(config["aspect_ratio"]))

    files_list = remove_random(files_list, nb_of_images - rows * cols)

    output_image = Image.new(
        "RGBA",
        (cols * fragment_side, rows * fragment_side),
        (255, 255, 255, 255)
    )

    count = 0

    for file in files_list:

            img = resize_input_image(
                Image.open(config["input_directory"] + "/" + file),
                fragment_side,
                fragment_side
            )

            col = count % cols
            row = count // cols
            offset = (int(col * fragment_side), int(row * fragment_side))

            output_image.paste(img, offset)

            count += 1

            prompt_progress(count, nb_of_images)

    output_image.save(config["output_image_file"])
