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
      if is_int(num):
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

  print("Configuration file {filename} was loaded".format(filename=filepath))
  return width, height, waters, woods, foods, golds

# -----------------------------Helper functions begin-----------------------------


# -------------------------File loading helper functions---------------------------
# helper function for detecting non integer character from string input
def is_int(s):
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

# -----------------------------helper functions for fundamental game rules-----------------------------


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

# -----------------------------helper functions for RECRUIT process-----------------------------


# Function that displays prices for recruiting armies
def display_prices():
  print("Recruit Prices:")
  print("  Spearman (S) - 1W, 1F")
  print("  Archer (A) - 1W, 1G")
  print("  Knight (K) - 1F, 1G")
  print("  Scout (T) - 1W, 1F, 1G")


# Function that checks if player has sufficient resources to recruit any units, return true for positive,
# false otherwise
def suffi_resource_check(flag, resources, prices):
  player_one_resource = {}
  player_two_resource = {}

  for key, value in resources.items():
    if key == "one":
      player_one_resource = value

    else:
      player_two_resource = value

  if flag:
    for army_price in prices:
      affordable_count = 0
      costs = prices[army_price]  # cost of a type of army (the inner dictionary)

      for c in costs:
        if costs[c] <= player_one_resource[c]:
          affordable_count += 1

      if affordable_count == len(costs):
        return True

    return False

  else:
    for army_price in prices:
      affordable_count = 0
      costs = prices[army_price]  # cost of a type of army (the inner dictionary)

      for c in costs:
        if costs[c] <= player_two_resource[c]:
          affordable_count += 1

      if affordable_count == len(costs):
        return True

    return False


# Function that checks if there are positions available around player's home base for army recruit, return
# True for positive result, False otherwise
def recruit_pos_check(flag, w, h):
  if flag:
    if game_map[1][ 0] == "  " or game_map[0][1] == "  " \
            or game_map[1][2] == "  " or game_map[1][2] == "  ":
      return True
  else:
    if game_map[h-2][w-3] == "  " or game_map[h-3][w-2] == "  " \
            or game_map[h-2][w-1] == "  " or game_map[h-1][w-2] == "  ":
      return True
  return False


# Function that checks if the passed position is next to this players homebase
def is_next_to_homebase(pos, flag, w, h):
  if flag:
    reserved1 = [["0", "1"], ["1", "0"], ["2", "1"], ["1", "2"]]

    if pos in reserved1:
      return True
    else:
      return False

  else:
    reserved2 = [[str(w - 3), str(h - 2)], [str(w - 2), str(h - 3)],
                 [str(w - 1), str(h - 2)], [str(w - 2), str(h - 1)]]

    if pos in reserved2:
      return True
    else:
      return False


# Function that checks if the passing position is valid for recruiting, return true for invalid position
def is_invalid_input_recruit(pos, w, h):
  if len(pos) != 2:
    return True
  x = pos[0]
  y = pos[1]

  if not is_int(x) or not is_int(y):
    return True

  if not 0 <= int(x) <= w-1 or not 0 <= int(y) <= h-1:
    return True
  return False

# -----------------------------helper functions for MOVE process-----------------------------


# Function that gets all the armies of current player ()
def get_armies_to_move(flag, this_map):
  player_army_one = {}
  player_army_two = {}

  if flag:
    for row in range(len(this_map)):
      for col in range(len(this_map[0])):
        temp = this_map[row][col]

        if temp[-1] == "1" and not temp[0] == "H":
          # store all the armies along with their positions
          if temp in player_army_one:
            player_army_one[temp].append((col, row))

          else:
            player_army_one[temp] = [(col, row)]
    return player_army_one

  else:
    for row in range(len(this_map)):
      for col in range(len(this_map[0])):
        temp = this_map[row][col]

        if temp[-1] == "2" and not temp[0] == "H":
          # store all the armies along with their positions
          if temp in player_army_two:
            player_army_two[temp].append((col, row))

          else:
            player_army_two[temp] = [(col, row)]
    return player_army_two


# Function that checks if this player has any units to move or not. return true for yes false otherwise
# (at the very first part when checking current player has any armies at all, should have called get_armies_to_move,
# that way can save a lot of running time when the game_map is huge, but since we are only dealing a max 7x7 game board
# I just left it this way)
def units_move_check(flag, this_map, movable_armies, w, h):
  player_army_one = {}
  player_army_two = {}
  resource_label = ["~~", "WW", "FF", "GG"]

  # If no armies to move
  count = 0
  for k, v in movable_armies.items():
    if not len(movable_armies[k]) == 0:
      count += 1

  if count == 0:
    return False

  # player 1
  if flag:
    # check are there any armies at all
    has_army = False
    for row in range(len(this_map)):
      for col in range(len(this_map[0])):
        temp = this_map[row][col]

        if temp[-1] == "1" and not temp[0] == "H":
          # store all the armies along with their positions
          if temp in player_army_one:
            player_army_one[temp].append((row, col))

          else:
            player_army_one[temp] = [(row, col)]

          has_army = True

    # return false if no armies at all
    if not has_army:
      return False
    else:
      # loop through every armies with their positions
      for army in player_army_one:
        for pos in player_army_one[army]:
          x = pos[0]
          y = pos[1]

          # do something else if this army is a scout
          if army[0] == "T":
            # get reachable positions (every positions within 2 steps from all four directions)
            pos_up_1 = (x - 1, y)
            pos_up_2 = (x - 2, y)
            pos_down_1 = (x + 1, y)
            pos_down_2 = (x + 2, y)
            pos_left_1 = (x, y - 1)
            pos_left_2 = (x, y - 2)
            pos_right_1 = (x, y + 1)
            pos_right_2 = (x, y + 1)
            neighbours = [pos_up_1, pos_up_2, pos_down_1, pos_down_2, pos_left_1, pos_left_2,
                          pos_right_1, pos_right_2]

            # remove invalid positions
            for n in neighbours:
              if n[0] < 0 or n[1] < 0:
                neighbours.remove(n)

            # check if any of the positions left is movable
            for position in neighbours:
              if this_map[position[0]][position[1]] == "  ":
                return True
              if this_map[position[0]][position[1]] in resource_label:
                return True
              if this_map[position[0]][position[1]][1] == "2":
                return True

          # check the position above
          if x - 1 < 0:
            pass
          else:
            pos_up = (x - 1, y)
            if this_map[pos_up[0]][pos_up[1]] == "  ": # check surrounding for spaces
              return True
            if this_map[pos_up[0]][pos_up[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_up[0]][pos_up[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check the position below
          if x + 1 > h - 1:
            pass
          else:
            pos_down = (x + 1, y)
            if this_map[pos_down[0]][pos_down[1]] == "  ":
              return True
            if this_map[pos_down[0]][pos_down[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_down[0]][pos_down[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check position to the left
          if y - 1 < 0:
            pass
          else:
            pos_left = (x, y - 1)
            if this_map[pos_left[0]][pos_left[1]] == "  ":
              return True
            if this_map[pos_left[0]][pos_left[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_left[0]][pos_left[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check position to the right
          if y + 1 > w - 1:
            pass
          else:
            pos_right = (x, y + 1)
            if this_map[pos_right[0]][pos_right[1]] == "  ":
              return True
            if this_map[pos_right[0]][pos_right[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_right[0]][pos_right[1]][1] == "2":  # check surrounding for countable enemies
              return True

  # player 2
  else:
    # check are there any armies at all
    has_army = False
    for row in range(len(this_map)):
      for col in range(len(this_map[0])):
        temp = this_map[row][col]

        if temp[-1] == "2" and not temp[0] == "H":
          # store all the armies along with their positions
          if temp in player_army_two:
            player_army_two[temp].append((row, col))

          else:
            player_army_two[temp] = [(row, col)]

          has_army = True

    # return false if no armies at all
    if not has_army:
      return False
    else:
      # loop through every armies with their positions
      for army in player_army_two:
        for pos in player_army_two[army]:
          x = pos[0]
          y = pos[1]

          # do something else if this army is a scout
          if army[0] == "T":
            # get reachable positions (every positions within 2 steps from all four directions)
            pos_up_1 = (x - 1, y)
            pos_up_2 = (x - 2, y)
            pos_down_1 = (x + 1, y)
            pos_down_2 = (x + 2, y)
            pos_left_1 = (x, y - 1)
            pos_left_2 = (x, y - 2)
            pos_right_1 = (x, y + 1)
            pos_right_2 = (x, y + 1)
            neighbours = [pos_up_1, pos_up_2, pos_down_1, pos_down_2, pos_left_1, pos_left_2,
                          pos_right_1, pos_right_2]

            # remove invalid positions
            for n in neighbours:
              if n[0] < 0 or n[1] < 0:
                neighbours.remove(n)

            # check if any of the positions left is movable
            for position in neighbours:
              if this_map[position[0]][position[1]] == "  ":
                return True
              if this_map[position[0]][position[1]] in resource_label:
                return True
              if this_map[position[0]][position[1]][1] == "1":
                return True

          # check the position above
          if x - 1 < 0:
            pass
          else:
            pos_up = (x - 1, y)
            if this_map[pos_up[0]][pos_up[1]] == "  ":  # check surrounding for spaces
              return True
            if this_map[pos_up[0]][pos_up[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_up[0]][pos_up[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check the position below
          if x + 1 > h - 1:
            pass
          else:
            pos_down = (x + 1, y)
            if this_map[pos_down[0]][pos_down[1]] == "  ":
              return True
            if this_map[pos_down[0]][pos_down[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_down[0]][pos_down[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check position to the left
          if y - 1 < 0:
            pass
          else:
            pos_left = (x, y - 1)
            if this_map[pos_left[0]][pos_left[1]] == "  ":
              return True
            if this_map[pos_left[0]][pos_left[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_left[0]][pos_left[1]][1] == "2":  # check surrounding for countable enemies
              return True

          # check position to the right
          if y + 1 > w - 1:
            pass
          else:
            pos_right = (x, y + 1)
            if this_map[pos_right[0]][pos_right[1]] == "  ":
              return True
            if this_map[pos_right[0]][pos_right[1]] in resource_label:  # check surrounding for resources
              return True
            if this_map[pos_right[0]][pos_right[1]][1] == "2":  # check surrounding for countable enemies
              return True
  return False


# Function that checks if the passing positions is valid for moving, return true for invalid position
def is_invalid_input_move(this_map, pos, w, h, flag):
  army_labels = ["S", "K", "A", "T"]

  # check format
  if len(pos) != 4:
    print("(Invalid format, four inputs are required!)")
    return True
  x1 = pos[0]
  y1 = pos[1]
  x2 = pos[2]
  y2 = pos[3]

  # check for integers
  if not is_int(x1) or not is_int(y1) or not is_int(x2) or not is_int(y2):
    print("(Invalid format, four integers are required!)")
    return True

  x1 = int(x1)
  y1 = int(y1)
  pos_start = [y1, x1]  # actual version indexes
  x2 = int(x2)
  y2 = int(y2)
  pos_end = [y2, x2]  # actual indexes in the 2D array

  # check for valid position
  if not 0 <= x1 <= w - 1 or not 0 <= y1 <= h - 1 \
          or not 0 <= x2 <= w - 1 or not 0 <= y2 <= h - 1:
    print("(Cannot move outside of game map!)")
    return True

  # check if pos 1 represents an army
  if not this_map[y1][x1][0] in army_labels:
    print("(This unit cannot be moved!)")
    return True

  army = this_map[y1][x1]  # the army on the board
  destination = this_map[y2][x2]  # the moving destination on the board
  army_one_step_away = [[y1-1, x1], [y1+1, x1], [y1, x1-1], [y1, x1+1]]  # positions that one step away from the army
  army_two_step_away = [[y1-2, x1], [y1+2, x1], [y1, x1-2], [y1, x1+2]]

  # store the army and its destination
  global start, end
  start = army
  end = destination

  # make sure the player only moves his own army
  if flag:
    if army[1] == "2":
      print("You cannot move other player's army!")
      return True
  else:
    if army[1] == "1":
      print("(You cannot move other player's army!)")
      return True
    pass

  # check for armies moving rule
  if army[0] == "S" or army[0] == "K" or army[0] == "A":
    # destination within one step ?
    if pos_end not in army_one_step_away:
      print("(This unit cannot reach the destiny!)")
      return True

    # check for allies
    if destination[1] == army[1]:
      print("(Cannot move to your own army or base!)")
      return True

  else:  # T
      # destination within two step ?
      if pos_end not in army_one_step_away:
        if pos_end not in army_two_step_away:
          print("(This unit cannot reach the destinyHAHA!)")
          return True

      # check for allies
      if destination[1] == army[1]:
        print("(Cannot move to your own army or base!)")
        return True

  return False


# Function that checks if army scout jumped over something
def jump_over_check(this_map, x1, y1, x2, y2):
  # 2-step positions
  two_step_pos = [(y1 - 2, x1), (y1 + 2, x1),
                  (y1, x1 - 2), (y1, x1 + 2)]

  # get rid of invalid positions
  for pos_two in two_step_pos:
    if pos_two[0] < 0 or pos_two[1] < 0 or \
            pos_two[0] > len(this_map) or pos_two[1] > len(this_map[0]):
      two_step_pos.remove(pos_two)

  # if destination is exact 2 step away
  if (y2, x2) in two_step_pos:
    # position that is one step away from starting point (The position that Scout jumps over)
    jumped_over_pos = ()

    # if destination is above starting point
    if y2 < y1:
      jumped_over_pos = (y1 - 1, x1)

    # if destination is under starting point
    elif y2 > y1:
      jumped_over_pos = (y1 + 1, x1)

    # if destination is on the left of starting point
    elif x2 < x1:
      jumped_over_pos = (y1, x1 - 1)

    # if destination is on the right of starting point
    else:
      jumped_over_pos = (y1, x1 + 1)

    global jumped_over_label
    global jumped_over_cord

    jumped_over_label = this_map[jumped_over_pos[0]][jumped_over_pos[1]]
    jumped_over_cord = jumped_over_pos

    return True

  else:
    return False

  # --------------------------------------Game loop (Main)---------------------------------------


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
  # -----------------------------turns begin---------------------------------
  play_again = True
  player_flag = True
  years = 617
  turn_count = 1
  players_resources = {"one": {"W": 2, "F": 2, "G": 2},
                       "two": {"W": 2, "F": 2, "G": 2}}
  recruit_prices = {"S": {"W": 1, "F": 1},
                    "A": {"W": 1, "G": 1},
                    "K": {"F": 1, "G": 1},
                    "T": {"W": 1, "F": 1, "G": 1}}

  army_names = {"S": "Spearman", "A": "Archer", "K": "Knight", "T": "Scout"}
  resource_names = {"WW": "Wood", "FF": "Food", "GG": "Gold"}

  while play_again:  # main loop, keep the game going turn by turn
    print("")
    print("-Year {}-".format(years))
    print("")
    if player_flag:
      print("+++Player 1's Stage: Recruit Armies+++")
    else:
      print("+++Player 2's Stage: Recruit Armies+++")
    print()
    if player_flag:
      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                 r2=players_resources["one"]["F"],
                                                                 r3=players_resources["one"]["G"]))
    else:
      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                 r2=players_resources["two"]["F"],
                                                                 r3=players_resources["two"]["G"]))

    # -------------------Recruit stage(step d)-----------------
    while True:
      # sufficient resource check
      if not suffi_resource_check(player_flag, players_resources, recruit_prices):
        print("No resources to recruit any armies")
        break
      # recruit position availability check
      if not recruit_pos_check(player_flag, width, height):
        print("No place to recruit new armies")
        break
      print()
      # ask for user input about recruitment type
      rec_type = input("Which type of army to recruit, (enter)'S', 'A', 'K', or 'T'? Enter 'No' to end "
                       "this stage\n")
      # d.i positive cases, valid input for army recruitment type
      if rec_type == "S" or rec_type == "A" or rec_type == "K" or rec_type == "T":

        # check for insufficient resources
        if player_flag:  # player one
          if rec_type == "S":
            # check for enough resource of recruiting a Spearman
            if players_resources["one"]["W"] == 0 or players_resources["one"]["F"] == 0:
              print("Insufficient resources. Try again!")
              continue

          elif rec_type == "A":
            # check for enough resource of recruiting a Archer
            if players_resources["one"]["W"] == 0 or players_resources["one"]["G"] == 0:
              print("Insufficient resources. Try again!")
              continue

          elif rec_type == "K":
            # check for enough resource of recruiting a Knight
            if players_resources["one"]["F"] == 0 or players_resources["one"]["G"] == 0:
              print("Insufficient resources. Try again!")
              continue

          else:
            # check for enough resource of recruiting a Scout
            if players_resources["one"]["W"] == 0 or players_resources["one"]["F"] == 0 \
                    or players_resources["one"]["G"] == 0:
                print("Insufficient resources. Try again!")
                continue

        else:  # player two
          if rec_type == "S":
            # check for enough resource of recruiting a Spearman
            if players_resources["two"]["W"] == 0 or players_resources["two"]["F"] == 0:
              print("Insufficient resources. Try again!")
              continue

          elif rec_type == "A":
            # check for enough resource of recruiting a Archer
            if players_resources["two"]["W"] == 0 or players_resources["two"]["G"] == 0:
              print("Insufficient resources. Try again!")
              continue

          elif rec_type == "K":
            # check for enough resource of recruiting a Knight
            if players_resources["two"]["F"] == 0 or players_resources["two"]["G"] == 0:
              print("Insufficient resources. Try again!")
              continue

          else:
            # check for enough resource of recruiting a Scout
            if players_resources["two"]["W"] == 0 or players_resources["two"]["F"] == 0 \
                    or players_resources["one"]["G"] == 0:
              print("Insufficient resources. Try again!")
              continue

        while True:  # recruitment position asking loop
          print(" ")
          rec_cord = input("You want to recruit a {}. Enter two integers as format 'x y' to place your "
                           "army: \n".format(army_names[rec_type]))

          if rec_cord == "QUIT":
            sys.exit("Game terminated")

          elif rec_cord == "DIS":
            display_map(game_map)
            continue

          elif rec_cord == "PRIS":
            display_prices()
            continue

          # check for invalid input
          elif is_invalid_input_recruit(rec_cord.split(), width, height):
            print("Sorry, invalid input. Try again!")
            continue

          # check if x y not next to home base or occupied
          elif not is_next_to_homebase(rec_cord.split(), player_flag, width, height) \
                  or not game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] == "  ":
            print("You must place your nearly recruited unit in an unoccupied position next to your"
                  "home base. Try again.")
            continue

          # Valid input and enough resource, recruit the desired army
          else:
            # -------------------------------player one's action-------------------------------------------
            if player_flag:
              # recruit SPEARMAN1
              if rec_type == "S":
                # apply the cost
                players_resources["one"]["W"] -= 1
                players_resources["one"]["F"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "S1"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print("")
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                           r2=players_resources["one"]["F"],
                                                                           r3=players_resources["one"]["G"]))
                break

              # recruit ARCHER1
              elif rec_type == "A":
                # apply the cost
                players_resources["one"]["W"] -= 1
                players_resources["one"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "A1"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print("")
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                           r2=players_resources["one"]["F"],
                                                                           r3=players_resources["one"]["G"]))
                break

              # recruit KNIGHT1
              elif rec_type == "K":
                # apply the cost
                players_resources["one"]["F"] -= 1
                players_resources["one"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "K1"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                           r2=players_resources["one"]["F"],
                                                                           r3=players_resources["one"]["G"]))
                break

              # recruit SCOUT1
              else:
                # apply the cost
                players_resources["one"]["W"] -= 1
                players_resources["one"]["F"] -= 1
                players_resources["one"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "T1"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                           r2=players_resources["one"]["F"],
                                                                           r3=players_resources["one"]["G"]))
                break

            # -------------------------------player TWO's action-------------------------------------------
            # recruit SPEARMAN2
            else:
              if rec_type == "S":
                # apply the cost
                players_resources["two"]["W"] -= 1
                players_resources["two"]["F"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "S2"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                           r2=players_resources["two"]["F"],
                                                                           r3=players_resources["two"]["G"]))
                break

              # recruit ARCHER2
              elif rec_type == "A":
                # apply the cost
                players_resources["two"]["W"] -= 1
                players_resources["two"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "A2"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                           r2=players_resources["two"]["F"],
                                                                           r3=players_resources["two"]["G"]))
                break

              # recruit KNIGHT2
              elif rec_type == "K":
                # apply the cost
                players_resources["two"]["F"] -= 1
                players_resources["two"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "K2"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                           r2=players_resources["two"]["F"],
                                                                           r3=players_resources["two"]["G"]))
                break

              # recruit SCOUT2
              else:
                # apply the cost
                players_resources["two"]["W"] -= 1
                players_resources["two"]["F"] -= 1
                players_resources["two"]["G"] -= 1

                # deploy the army
                game_map[int(rec_cord.split()[1])][int(rec_cord.split()[0])] = "T2"

                # print feedback
                print("")
                print("You has recruited a {}.".format(army_names[rec_type]))
                print()
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                           r2=players_resources["two"]["F"],
                                                                           r3=players_resources["two"]["G"]))
                break

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

    # -----------------------------Move stage(step e)---------------------------
    print()
    if player_flag:
      print("===Player 1's Stage: Move Armies===")
    else:
      print("===Player 2's Stage: Move Armies===")

    # store the positions that have already been used as destination
    moved_pos = []
    r_n_s_label = ["  ", "~~", "WW", "FF", "GG"]
    counters = {"S": "K", "K": "A", "A": "S"}
    armies_to_move = get_armies_to_move(player_flag, game_map)

    while True:
      print()
      # check for units moving ability and print armies to move if there are any
      if units_move_check(player_flag, game_map, armies_to_move, width, height):
        print("Armies to Move:")
        for key, value in armies_to_move.items():
          name = str(key[0])
          pos = ""
          for tuples in armies_to_move[key]:
            pos += str(tuples) + " "

          if not pos == "":
            print(" {a}:{b}".format(a=army_names[name], b=pos))
        print("")
        # Ask player for moving positions
        move_cord = input("Enter four integers as a format 'x0 y0 x1 y1' to represent move unit from "
                          "(x0, y0) to (x1, y1) or 'No' to end this turn.")

        # these two variable which stores label for the moving army and its destination will be updated
        # in function is_invalid_input_move(game_map, move_cord.split(), width, height, player_flag)
        start = ""
        end = ""

        if move_cord == "QUIT":
          sys.exit("Game terminated")

        elif move_cord == "DIS":
          display_map(game_map)

        elif move_cord == "PRIS":
          display_prices()

        elif move_cord == "NO":
          break

        # check for invalid input
        elif is_invalid_input_move(game_map, move_cord.split(), width, height, player_flag):
          print("Sorry, invalid input. Try again!")

        # make sure every armies only moves once in each turn
        elif (move_cord.split()[0], move_cord.split()[1]) in moved_pos:
          print("Sorry, your armies can only move once in each turn.")

        # apply move result
        else:
          # print move result
          print("")
          print("You have moved {name} from ({x1},{y1}) to ({x2},{y2})".
                format(name=army_names[start[0]], x1=move_cord.split()[0], y1=move_cord.split()[1],
                       x2=move_cord.split()[2], y2=move_cord.split()[3]))

          # the input indexes
          start_pos_x = int(move_cord.split()[0])
          start_pos_y = int(move_cord.split()[1])
          end_pos_x = int(move_cord.split()[2])
          end_pos_y = int(move_cord.split()[3])

          # records the destination and remove it from armies to move
          moved_pos.append((end_pos_x, end_pos_y))
          armies_to_move[start].remove((start_pos_x, start_pos_y))

          # updates game board

          # when destination was space or resources or waters
          if end in r_n_s_label:
            # check if Scout jumps over an enemy
            if start[0] == "T":
              jumped_over_label = ""  # will be updated in function jump_over_check
              jumped_over_cord = ()
              # if T moved 2 steps

              if jump_over_check(game_map, start_pos_x, start_pos_y, end_pos_x, end_pos_y):

                # if T jumped over an enemy army
                if jumped_over_label[0] in army_names.keys() and jumped_over_label[1] == start[1]:
                  game_map[start_pos_y][start_pos_x] = "  "
                  print("We lost the army Scout due to your command!")

                # if T jumped over a resource (collect both of them and print 2 messages)
                elif jumped_over_label in ["WW", "GG", "FF"]:
                  # player one
                  if player_flag:
                    # if jumps over resource to reach a resource:
                    if end in ["WW", "GG", "FF"]:
                      # update game board
                      game_map[start_pos_y][start_pos_x] = "  "
                      game_map[end_pos_y][end_pos_x] = start
                      game_map[jumped_over_cord[0]][jumped_over_cord[1]] = "  "

                      # update resources
                      players_resources["one"][end[0]] += 2
                      players_resources["one"][jumped_over_label[0]] += 2
                      print("Good. We collected 2 {}.".format(resource_names[end]))
                      print("Good. We collected 2 {}.".format(resource_names[jumped_over_label]))
                      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                                 r2=players_resources["one"]["F"],
                                                                                 r3=players_resources["one"]["G"]))
                      continue

                    # if jumps over resource to reach a space
                    elif end == "  ":
                      # update game board
                      game_map[start_pos_y][start_pos_x] = "  "
                      game_map[end_pos_y][end_pos_x] = start
                      game_map[jumped_over_cord[0]][jumped_over_cord[1]] = "  "

                      # update resources
                      players_resources["one"][jumped_over_label[0]] += 2
                      print("Good. We collected 2 {}.".format(resource_names[jumped_over_label]))
                      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                                 r2=players_resources["one"]["F"],
                                                                                 r3=players_resources["one"]["G"]))
                      continue

                  # player two
                  else:
                    # if jumps over resource to reach a resource:
                    if end in ["WW", "GG", "FF"]:
                      # update game board
                      game_map[start_pos_y][start_pos_x] = "  "
                      game_map[end_pos_y][end_pos_x] = start
                      game_map[jumped_over_cord[0]][jumped_over_cord[1]] = "  "

                      # update resources
                      players_resources["two"][end[0]] += 2
                      players_resources["two"][jumped_over_label[0]] += 2
                      print("Good. We collected 2 {}.".format(resource_names[end]))
                      print("Good. We collected 2 {}.".format(resource_names[jumped_over_label]))
                      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                                 r2=players_resources["two"]["F"],
                                                                                 r3=players_resources["two"]["G"]))
                      continue

                    # if jumps over resource to reach a space
                    elif end == "  ":
                      # update game board
                      game_map[start_pos_y][start_pos_x] = "  "
                      game_map[end_pos_y][end_pos_x] = start
                      game_map[jumped_over_cord[0]][jumped_over_cord[1]] = "  "

                      # update resources
                      players_resources["two"][jumped_over_label[0]] += 2
                      print("Good. We collected 2 {}.".format(resource_names[jumped_over_label]))
                      print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                                 r2=players_resources["two"]["F"],
                                                                                 r3=players_resources["two"]["G"]))
                      continue

                # if T jumps over water
                elif jumped_over_label == "~~":
                  game_map[start_pos_y][start_pos_x] = "  "
                  print("We lost the army {} due to your command!".format(army_names[start[0]]))
                  continue

                # if T jumps over space
                else:
                  pass

              else:
                pass

            else:  # do nothing
              pass

            # move to space
            if end == "  ":
              game_map[start_pos_y][start_pos_x] = "  "
              game_map[end_pos_y][end_pos_x] = start

            # water destroys army
            elif end == "~~":
              game_map[start_pos_y][start_pos_x] = "  "
              print("We lost the army {} due to your command!".format(army_names[start[0]]))

            # collect resources
            else:
              game_map[start_pos_y][start_pos_x] = "  "
              game_map[end_pos_y][end_pos_x] = start
              # store the resource
              if player_flag:
                players_resources["one"][end[0]] += 2
                print("Good. We collected 2 {}.".format(resource_names[end]))
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["one"]["W"],
                                                                           r2=players_resources["one"]["F"],
                                                                           r3=players_resources["one"]["G"]))
              else:
                players_resources["two"][end[0]] += 2
                print("Good. We collected 2 {}.".format(resource_names[end]))
                print("[Your Asset: Wood-{r1} Food-{r2} Gold-{r3}]".format(r1=players_resources["two"]["W"],
                                                                           r2=players_resources["two"]["F"],
                                                                           r3=players_resources["two"]["G"]))
                print("")

          # when destination was enemy armies
          else:
            end_label = end[0]
            start_label = start[0]

            # T
            if start_label == "T":
              # when T encounters enemy T
              if end_label == "T":
                game_map[start_pos_y][start_pos_x] = "  "
                game_map[end_pos_y][end_pos_x] = "  "
                print("Great! We defeated the enemy {} with massive loss!".format(army_names[end_label]))
                continue

              # when T encounters enemy Army
              elif end_label in ["S", "A", "K"]:
                game_map[start_pos_y][start_pos_x] = "  "
                print("We lost the army {} due to your command!".format(army_names[start_label]))
                continue

              # when T reaches enemy base
              else:
                print("The army {} captured the enemy's capital".format(army_names[start_label]))
                print("")
                commander_name = input("What's your name, commander?")
                print(" ")
                print("***Congratulation! Emperor {a} unified the country in {b}.***".format(a=commander_name, b=years))
                sys.exit("The game is finished!")

            # encounters an enemy that counters player's army (player's army disappear)
            if counters[end_label] == start_label:
              game_map[start_pos_y][start_pos_x] = "  "
              print("We lost the army {} due to your command!".format(army_names[start_label]))

            # encounters a counter enemy (take down the enemy)
            elif counters[start_label] == end_label:
              game_map[start_pos_y][start_pos_x] = "  "
              game_map[end_pos_y][end_pos_x] = start
              print("Great! We defeated the enemy {}.".format(army_names[end_label]))

            # encounters a same type of enemy (both disappear)
            elif start_label == end_label:
              game_map[start_pos_y][start_pos_x] = "  "
              game_map[end_pos_y][end_pos_x] = "  "
              print("Great! We defeated the enemy {} with massive loss!".format(army_names[end_label]))

            # encounters home base of other player
            else:
              print("The army {} captured the enemy's capital".format(army_names[start_label]))
              print("")
              commander_name = input("What's your name, commander?")
              print(" ")
              print("***Congratulation! Emperor {a} unified the country in {b}.***".format(a=commander_name, b=years))
              sys.exit()

      else:  # if player has no units to move
        print("No Army to Move: next turn")
        print()
        break

    # end of turn, flip the flag and increment the year
    player_flag = not player_flag
    if turn_count % 2 == 0:
      years += 1
    turn_count += 1


