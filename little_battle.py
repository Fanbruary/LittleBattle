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

    # remove all empty lines
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

    # ------------------------------------check file content-----------------------------
    for lines in contents_list:
        print(lines.split())

    # check the content of Frame
    frame = contents_list[0].split()
    if len(frame) != 2:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")

    # check for x
    if "x" in frame[1]:
        width_and_height = frame[1].split("x")
    else:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")
    print(width_and_height)

    # check for weight x height format
    if '' in width_and_height or len(width_and_height) > 2:
        raise SyntaxError("Invalid Configuration File: frame should be in format width x height")

    # check for the range of width and height
    if not 5 <= int(width_and_height[0]) <= 7 or not 5 <= int(width_and_height[1]) <= 7:
        raise ArithmeticError("Invalid Configuration File: width and height should range from 5 to 7")


    print("Success!")

    return width, height, waters, woods, foods, golds




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    try:
        width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
    except FileNotFoundError:
        print("Warning: no such file founded")