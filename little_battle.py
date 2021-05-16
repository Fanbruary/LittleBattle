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
    raise SyntaxError("Invalid Configuration File: Format error! exact five lines are expected")

  # check for required labels
  for line in contents_list:
    if line.split()[0] not in label_check:
      raise SyntaxError("Invalid Configuration File: Format error! unexpected label detected!")

  # ------------------------------------check the content of Frame-----------------------------
  # check there are only one set of weight and height
  frame = contents_list[0].split()
  if len(frame) != 2:
    raise SyntaxError("Invalid Configuration File: Frame should be in format width x height")

  # check for x
  if "x" in frame[1]:
    width_and_height = frame[1].split("x")
  else:
    raise SyntaxError("Invalid Configuration File: Frame should be in format width x height")

  # check for weight x height format
  if '' in width_and_height or len(width_and_height) > 2:
    raise SyntaxError("Invalid Configuration File: Frame should be in format width x height")

  # check for the range of width and height
  if not 5 <= int(width_and_height[0]) <= 7 or not 5 <= int(width_and_height[1]) <= 7:
    raise ArithmeticError("Invalid Configuration File: Width and height should range from 5 to 7")

  # store width and height
  width = int(width_and_height[0])
  height = int(width_and_height[1])

  # -------------------------check the second line to the last line-----------------------------
  second_to_last_lines = contents_list[1:]  # list that contains all of the raw data except the first line (frame)

  # check for non int characters and turn "second_to_last_lines" into a binary list
  for i in range(len(second_to_last_lines)):
    second_to_last_lines[i] = second_to_last_lines[i].split()  # convert lines into lists
    for num in second_to_last_lines[i][1:]:
      if detect_int(num):
        continue
      else:
        raise ValueError("Invalid Configuration File: " + second_to_last_lines[i][0][:-1] + " Contains non "
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

  # check for odd number of elements
  for line in second_to_last_lines:
    if len(line) % 2 == 0:
      raise SyntaxError("Invalid Configuration File: " + line[0][:-1] + " Has an odd number of elements!")

  # check for valid position
  for line in second_to_last_lines:
    # check widths are valid
    for num in line[1::2]:
      if not 0 <= int(num) <= width - 1:
        raise ArithmeticError("Invalid Configuration File: " + line[0][:-1] + " Contains a position that "
                                                                              "is out of map.")
    # check height are valid
    for num_h in line[2::2]:
      if not 0 <= int(num_h) <= height - 1:
        raise ArithmeticError("Invalid Configuration File: " + line[0][:-1] + " Contains a position that "
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

  print("width: ", width)
  print("height: ", height)
  print("Water: ", waters)
  print("Wood: ", woods)
  print("Food: ", foods)
  print("Gold: ", golds)
  print("")
  print("Configuration file {filename} was loaded".format(filename=filepath))
  return width, height, waters, woods, foods, golds


# helper function for detecting non integer character
def detect_int(s):
  try:
    int(s)
    return True
  except (ValueError, TypeError):
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


# Function that displays the game board
def display_map(this_map):
  w = len(this_map[0])
  h = len(this_map)
  x_index_row = []
  y_index_column = []
  y_border_row = ""
  num_of_dash = w * 2 + w - 1

  # generate the first row (indexes for x)
  for i in range(w):
    if i == 0:
      x_index_row.append("X{}0".format(str(i)))
    elif i == w - 1:
      x_index_row.append("0{}X".format(str(i)))
    else:
      x_index_row.append("0" + str(i))

  # generate y indexes
  for i in range(h):
    y_index_column.append("0{}".format(str(i)))

  # generate the border row
  y_border_row = " Y+{dashes}+".format(dashes=num_of_dash * "-")

  print("Please check the battlefield, commander")

  # print the map
  print("  " + " ".join(x_index_row))
  print(y_border_row)

  for i in range(len(this_map)):
    print(y_index_column[i], end="")
    for c in this_map[i]:
      print("|" + c, end="")
    print("|", end="")
    print()

  print(y_border_row)
  print("(enter DIS to display the map)")
  print()

  return


# Function that load the resource and generate game board
def generate_map(w, h, waters1, woods1, foods1, golds1):
  # generate 2D array game board
  this_map = [["  " for i in range(w)] for j in range(h)]

  # load resource positions
  for pos in waters1:
    index_x = int(pos[0])
    index_y = int(pos[1])
    this_map[index_y][index_x] = "~~"

  for pos in woods1:
    index_x = int(pos[0])
    index_y = int(pos[1])
    this_map[index_y][index_x] = "WW"

  for pos in foods1:
    index_x = int(pos[0])
    index_y = int(pos[1])
    this_map[index_y][index_x] = "FF"

  for pos in golds1:
    index_x = int(pos[0])
    index_y = int(pos[1])
    this_map[index_y][index_x] = "GG"

  # load home bases of 2 players
  this_map[1][1] = "H1"
  this_map[h - 2][w - 2] = "H2"

  return this_map


# displays prices for recruiting armies
def display_prices():
  print("Recruit Prices:")
  print("  Spearman (S) - 1W, 1F")
  print("  Archer (A) - 1W, 1G")
  print("  Knight (K) - 1F, 1G")
  print("  Scout (T) - 1W, 1F, 1G")


# Check if player has sufficient resources to recruit any units, return true for positive, false otherwise
def suffi_resource_check():
  return True


# Check if there are positions available around player's home base for army recruit, return True for
# positive result, False otherwise
def recruit_pos_check():
  return True


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 little_battle.py config.txt")
    sys.exit()
  try:
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
  except FileNotFoundError:
    print("Warning: no such file founded")

  # -----------------------------game starts---------------------------------
  print("Game Started: Little Battle! (enter QUIT to quit the game)")
  print("")
  game_map = generate_map(width, height, waters, woods, foods, golds)
  display_map(game_map)
  display_prices()
  print("(enter PRIS to display the price list)")
  print("")
  # -----------------------------turns begin---------------------------------
  play_again = True
  player_one = True
  years = 617
  player_one_resources = {"Wood": 1, "Food": 2, "Gold": 3}
  player_two_resources = {"Wood": 1, "Food": 2, "Gold": 3}
  army_names = {"S": "Spearman", "A": "Archer", "K": "Knight", "T": "Scout"}

  while play_again:  # main loop, keep the game going turn by turn
    print("-Year {}-".format(years))
    print("")
    if player_one:
      print("+++Player 1's Stage: Recruit Armies+++")
    else:
      print("+++Player 2's Stage: Recruit Armies+++")
    print()
    print("[Your Asset: Wood-1 Food-2 Gold-3]")

    # -------------------Recruit stage(step d)-----------------
    while True:
      # sufficient resource check
      if not suffi_resource_check():
        print("No resources to recruit any armies")
        break
      # recruit position availability check
      if not recruit_pos_check():
        print("No place to recruit new armies")
        break
      print()
      # ask for user input about recruitment type
      rec_type = input("Which type of army to recruit, (enter)'S', 'A', 'K', or 'T'? Enter 'No' to end "
                       "this stage: ")
      # d.i positive cases, valid input for army recruitment type
      if rec_type == "S" or rec_type == "A" or rec_type == "K" or rec_type == "T":
        print(" ")
        rec_cord = input("You want to recruit a {}. Enter two integers as format 'x y' to place your "
                         "army: ".format(army_names[rec_type]))
        rec_cord.split()

        rec_x = rec_cord.split()[0]
        rec_y = rec_cord.split()[1]

        print("rec_cord: " + rec_cord)
        print(rec_x)
        print(rec_y)

        if rec_cord == "QUIT":
          sys.exit("Game terminated")

        elif rec_cord == "DIS":
          display_map(game_map)

        elif rec_cord == "PRIS":
          display_prices()

        elif game_map[int(rec_y)][int(rec_x)] == "  ":  # positive cases for recruit position
          print("success")
          pass
        else:
            print("Sorry, invalid input. Try again")

      # d.iii Edge cases
      elif rec_type == "NO":
        break

      elif rec_type == "QUIT":
        sys.exit("Game terminated")

      elif rec_type == "DIS":
        display_map(game_map)

      elif rec_type == "PRIS":
        display_prices()

      else:
        print("Sorry, invalid input. Try again")  # d.ii Negative cases
    # 5e
