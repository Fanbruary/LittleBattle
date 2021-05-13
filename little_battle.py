import sys
# Please implement this function according to Section "Read Configuration File"


def load_config_file(filepath):
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], []  # list of position tuples
    label_check = ["Frame:", "Water:", "Wood:", "Food:", "Gold:"]  # label list
    contents_list = []  # list that contains all the input data (everything raw)
    positions = []  # List that only contains positions

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
    second_to_last_lines = contents_list[1:] # list that contains all of the raw data except the first line (frame)
    # print("second_to_last_lines: ")
    # print(second_to_last_lines)

    # check for non int characters and turn "second_to_last_lines" into a binary list
    for i in range(len(second_to_last_lines)):
        second_to_last_lines[i] = second_to_last_lines[i].split()  # convert lines into lists
        for num in second_to_last_lines[i][1:]:
            if detect_int(num):
                continue
            else:
                raise ValueError("Invalid Configuration File: " + second_to_last_lines[i][0][:-1] + "contains non "
                                                                                                    "integer "
                                                                                                    "characters!")
    # store the resource locations into "positions" (positions only, discard the labels)
    for resource_lists in second_to_last_lines:
        resource_name = resource_lists[0][:-1]
        resource_position = resource_lists[1:]

        if resource_name == "Water":
            positions.append(resource_position)

        elif resource_name == "Wood":
            positions.append(resource_position)

        elif resource_name == "Food":
            positions.append(resource_position)

        elif resource_name == "Gold":
            positions.append(resource_position)

    # print("EVery resources cord:")
    # print(waters)
    # print(woods)
    # print(foods)
    # print(golds)
    # print("positions: ")
    # print(positions)
    # print("")

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

    # convert list of positions into list of position tuples
    for i in range(len(positions)):
        x_cord = positions[i][0::2]
        y_cord = positions[i][1::2]
        positions[i] = list(zip(x_cord, y_cord))  # a list of position tuples

    # store these position tuples
    waters = positions[0]
    woods = positions[1]
    foods = positions[2]
    golds = positions[3]

    # print("New positions")
    # print(positions)

    # check for reserved position
    for p in positions:
        result = check_reserved_p(p, width, height)
        if result:
            continue
        else:
            raise ValueError("Invalid Configuration File: The positions of home bases or the positions"
                             " next to the home bases are occupied !")

    # check for duplicated resource positions
    count_list = []
    duplicate_list = []
    for list_t in positions:
        for t in list_t:
            if t not in count_list:
                count_list.append(t)
            else:
                duplicate_list.append(t)

    duplicate_list = list(set([i for i in duplicate_list]))
    if len(duplicate_list) != 0:
        raise SyntaxError("Invalid Configuration File: Duplicate position {cord}".format(cord=duplicate_list))

    print(width)
    print(height)
    print(waters)
    print(woods)
    print(foods)
    print(golds)
    print("Configuration file {filename} was loaded".format(filename=filepath))
    return width, height, waters, woods, foods, golds


# helper function for detecting non integer character
def detect_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# helper function for checking the reserved position. Return a boolean that indicates whether the input resource
# positions contains a reserved position or not. Will return True if the input list is clear, False otherwise.
def check_reserved_p(list_t, width, height):
    # define the reserved cords lists
    home_bases = [("1", "1"), (str(width - 2), str(height - 2))]
    surrounding_p = [("0", "1"), ("1", "0"), ("2", "1"), ("1", "2"), (str(width - 3), str(height - 2)),
                     (str(width - 2), str(height - 3)), (str(width - 1), str(height - 2)),
                     (str(width - 2), str(height - 1))]
    result = True
    # print(home_bases)
    # print(surrounding_p)
    # print("")
    # print(list_t)

    for cord in list_t:
        if cord in home_bases or cord in surrounding_p:
            result = False
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py config.txt")
        sys.exit()
    try:
        width_new, height_new, waters_new, woods_new, foods_new, golds_new = load_config_file(sys.argv[1])
    except FileNotFoundError:
        print("Warning: no such file founded")
