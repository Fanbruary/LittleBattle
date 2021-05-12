import sys

# Please implement this function according to Section "Read Configuration File"


def load_config_file (filepath):
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], [] # list of position tuples
    label_check = ["Frame:", "Water:", "Wood:", "Food:", "Gold:"]
    contents_list = []

    # read contents from config file
    f = open(filepath)
    contents = f.readlines()
    f.close()

    # ------------------------------------check file format------------------------------------

    # remove all empty lines and store the data in content_list
    for line in contents:
        if not line.strip():  # empty sequences detected
            continue
        else:
            contents_list.append(line.rstrip("\n"))

    # check there are only five lines
    if len(contents_list) != 5:
        raise SyntaxError("Invalid Configuration File: format error! exact five lines are expected")

    # check for required labels
    for line in contents_list:
        if line.split()[0] not in label_check:
            raise SyntaxError("Invalid Configuration File: format error! unexpected label detected!")

    # ------------------------------------check the content of Frame-----------------------------
    # debug
    # for lines in contents_list:
    #     print(lines.split())

    # check there are only one set of weight and height
    frame = contents_list[0].split()
    if len(frame) != 2:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")

    # check for x
    if "x" in frame[1]:
        width_and_height = frame[1].split("x")
    else:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")

    # check for weight x height format
    if '' in width_and_height or len(width_and_height) > 2:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")

    # check for the range of width and height
    if not 5 <= int(width_and_height[0]) <= 7 or not 5 <= int(width_and_height[1]) <= 7:
        raise ArithmeticError("Invalid Configuration File: width and height should range from 5 to 7")

    # store width and height
    width = int(width_and_height[0])
    height = int(width_and_height[1])

    # -------------------------check the second line to the last line-----------------------------
    second_to_last_lines = contents_list[1:]
    print(second_to_last_lines)

    # check for non int characters and turn second_to_last_lines into a binary list
    for i in range(len(second_to_last_lines)):
        second_to_last_lines[i] = second_to_last_lines[i].split()   # convert lines into lists
        for num in second_to_last_lines[i][1:]:
            if detect_int(num):
                continue
            else:
                raise ValueError("Invalid Configuration File: " + second_to_last_lines[i][0][:-1] + "contains non "
                                                                                                    "integer "
                                                                                                    "characters!")
    # store the resource locations
    for resource_lists in second_to_last_lines:
        resource_name = resource_lists[0][:-1]
        resource_position = resource_lists[1:]

        if resource_name == "Water":
            waters = resource_position
        elif resource_name == "Wood":
            woods = resource_position
        elif resource_name == "Food":
            foods = resource_position
        elif resource_name == "Gold":
            golds = resource_position

    print(waters)
    print(woods)
    print(foods)
    print(golds)

    # check for odd number of elements
    for line in second_to_last_lines:
        if len(line) % 2 == 0:
            raise ValueError("Invalid Configuration File: " + line[0][:-1] + " has an odd number of elements!")

    # check for valid position
    for line in second_to_last_lines:
        # check widths are valid
        for num in line[1::2]:
            if not 0 <= int(num) <= width - 1:
                raise ArithmeticError("Invalid Configuration File: " + line[0][:-1] + " contains a position that "
                                                                                      "is out of map.")
        # check height are valid
        for num_h in line[2::2]:
            if not 0 <= int(num_h) <= height - 1:
                raise ArithmeticError("Invalid Configuration File: " + line[0][:-1] + " contains a position that "
                                                                                      "is out of map.")
    # check for reserved position



    print("Success!")

    return width, height, waters, woods, foods, golds


# helper function for detecting non integer character
def detect_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# helper function for checking reserved position
def check_reserved_p(list_p, width, height):
    


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    try:
        width_new, height_new, waters_new, woods_new, foods_new, golds_new = load_config_file(sys.argv[1])
    except FileNotFoundError:
        print("Warning: no such file founded")