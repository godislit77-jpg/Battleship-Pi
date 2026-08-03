import random

def print_horizontal(block_left, block_right, padding):
    result = "" 
    for line in range(len(block_left.split("\n"))):
            result += f"{block_left.split("\n")[line]}{" " * padding}{block_right.split("\n")[line]}\n"
    print(result)

def collect_intput(query, max=float("inf"), min=float("-inf"), error="You entered an invalid input. Please try again.", ):
    while(True):
        intput = ""
        try:
            intput = int(input(query))
            if max >= intput >= min:
                return intput
            print(error)
        except ValueError:
            print(error)

def collect_stringput(query, valid_values=None, invalid_values=None, case_sensitive=True, valid_error="You entered an invalid input. Please try again.", invalid_error="You entered an invalid input. Please try again."):
    while True:
        user_input = input(query)

        clean_input = user_input if case_sensitive else user_input.lower()
        
        def stringify(iterable):
            return {str(x) if case_sensitive else str(x).lower() for x in iterable}

        if invalid_values and clean_input in stringify(invalid_values):
            print(invalid_error)
        elif valid_values and clean_input not in stringify(valid_values):
            print(valid_error)
        else:
            return user_input
        
def num_end(num):
    if num % 100 == 12:
        end = 'th'
    else:
        end = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    
    return f"{num}{end}"

def bracket_dict_values(dictionary):
    bracketted = {}
    sorted_dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    balanced_rank = 0
    rank = 0
    for key, value in sorted_dictionary:
        if not bracketted.get(rank) or value != bracketted.get(rank)["value"]:
            rank += 1
            bracketted.update({rank: {"keys": [key], "value": value, "balanced_rank": rank}})
            if rank > 1:
                balanced_rank += len(bracketted[rank - 1]["keys"])
                bracketted[rank]["balanced_rank"] = balanced_rank
        else:
            bracketted[rank]["keys"].append(key)
    return bracketted

def get_bracket_ranking(value, bracketted_dictionary):
    for keys in bracketted_dictionary.values():
        if value in keys["keys"]:
            return keys["balanced_rank"]
    return -1
        
def greatest_dict_values(dictionary):
    sorted_list = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)

    tied = []

    for key, value in sorted_list:
        if value == sorted_list[0][1]:
            tied.append(key)
        else: break
    return tied

def to_cell(row, col):
        return f"{chr(65+row)}{col+1}"

def get_health(board, name):
    health = []
    for row in board:
        for cell in row:
            if cell["name"] == name:
                if cell["hit"]:
                    health.append(False)
                else:
                    health.append(True)
    return health


def sniff_ship(board, player):
    offsets = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    inverse_directions = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }

    potential_guesses = []
    num_rows = len(board[player])
    num_cols = len(board[player][0])

    for row in range(num_rows):
        for col in range(num_cols):
            cell = board[player][row][col]
            ship_name = cell['name']
            
            if ship_name != 'empty' and cell['hit']:
                sunk = True
                segments_hit = 0
                for segment in get_health(board[player], ship_name):
                    if segment:
                        sunk = False
                    else:
                        segments_hit += 1
                        
                if not sunk:
                    orientation = 'unknown'
                    if segments_hit >= 2:
                        for check_direction_key, (offset_row, offset_col) in offsets.items():
                            if orientation != 'unknown':
                                break
                            neighbor_row = row + offset_row
                            neighbor_col = col + offset_col
                            if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols:
                                neighbor = board[player][neighbor_row][neighbor_col]
                                if neighbor['hit'] and neighbor['name'] == ship_name:
                                    orientation = 'vertical' if check_direction_key in ['UP', 'DOWN'] else 'horizontal'

                    modified_cells = []
                    for row_idx in range(num_rows):
                        for cell_idx in range(num_cols):
                            if board[player][row_idx][cell_idx]['name'] == ship_name and board[player][row_idx][cell_idx]['hit']:
                                board[player][row_idx][cell_idx]['hit'] = False
                                modified_cells.append((row_idx, cell_idx))

                    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                        if orientation == 'horizontal' and direction in ['UP', 'DOWN']:
                            continue
                        if orientation == 'vertical' and direction in ['LEFT', 'RIGHT']:
                            continue
                        
                        target_row = row + offsets[direction][0]
                        target_col = col + offsets[direction][1]

                        can_fit = False
                        
                        inverse_dir = inverse_directions[direction]
                        back_row_offset, back_col_offset = offsets[inverse_dir]

                        for i in range(cell["length"]):
                            start_row = row + (back_row_offset * i)
                            start_col = col + (back_col_offset * i)
                            
                            if check_direction(player, board, cell, to_cell(start_row, start_col), direction, True):
                                can_fit = True
                                break
                            
                        if can_fit:
                            if 0 <= target_row < num_rows and 0 <= target_col < num_cols:
                                target_cell = board[player][target_row][target_col]
                                target_was_hit = target_cell['hit'] or (target_row, target_col) in modified_cells
                                if not target_was_hit:
                                    target_string = chr(65 + target_row) + str(target_col + 1)
                                    if target_string not in potential_guesses:
                                        potential_guesses.append(target_string)

                    for row_idx, cell_idx in modified_cells:
                        board[player][row_idx][cell_idx]['hit'] = True

    return potential_guesses

def hard_computer_guesses(board, other_player, ships, return_shippability=False):
    cell_shippability = {}
    for row_idx, row in enumerate(board[other_player]):
        for cell_idx, _ in enumerate(row):
            cell = to_cell(row_idx, cell_idx)
            cell_shippability.setdefault(cell, 0)

    guaranteed_ships = sniff_ship(board, other_player)
    
    for row_idx, row in enumerate(board[other_player]):
        for cell_idx, cell_info in enumerate(row):
            if cell_info["hit"]: 
                cell_shippability[to_cell(row_idx, cell_idx)] = -1
            else:
                cell = to_cell(row_idx, cell_idx)
                for ship in ships:
                    if True in get_health(board[other_player], ship["name"]):
                        if check_direction(other_player, board, ship, cell, "DOWN", True):
                            for i in range(ship["length"]):
                                covered_cell = to_cell(row_idx + i, cell_idx)
                                if -1 < cell_shippability[covered_cell]:
                                    cell_shippability[covered_cell] += 1
                                
                        if check_direction(other_player, board, ship, cell, "RIGHT", True):
                            for i in range(ship["length"]):
                                covered_cell = to_cell(row_idx, cell_idx + i)
                                if -1 < cell_shippability[covered_cell]:
                                    cell_shippability[covered_cell] += 1

    if guaranteed_ships:
        for guess in guaranteed_ships:
            if -1 < cell_shippability[guess]:
                cell_shippability[guess] += 1000

    if return_shippability: 
        return cell_shippability

    if random.randint(0, 4) < 3 and len(guaranteed_ships) == 0:
        for cell in greatest_dict_values(cell_shippability):
            if cell in cell_shippability:
                cell_shippability.pop(cell)
        return greatest_dict_values(cell_shippability)

    return greatest_dict_values(cell_shippability)

def shoot(other_player, guess, board, tactical, current_player):
    row, col = convert_guess(guess)
    ship_info = board[other_player][row][col]["name"]
    board[other_player][row][col]["hit"] = True
    if ship_info == 'empty':
        print(f"{guess} is a miss!")
        return False
    print(f"{guess} is a hit on player {other_player + 1}'s {ship_info}!\n")
    if True not in get_health(board[other_player], ship_info):
        if tactical:
            tactical_obliteration(other_player, board, ship_info)
        print(f"Player {current_player+1} sunk a {ship_info}")
    return True

def tactical_obliteration(player, board, id):
    for row_idx, row in enumerate(board[player]):
        for cell_idx, cell in enumerate(row):
            if cell["name"] == id:
                surroundings = [-1, 0, 1]
                for spot_row in surroundings:
                    for spot_col in surroundings:
                        if spot_col == -1 and cell_idx < 1: continue
                        if spot_row == -1 and row_idx < 1: continue
                        if spot_col == 1 and cell_idx >= len(row) - 1: continue
                        if spot_row == 1 and row_idx >= len(board[player]) - 1: continue
                        if board[player][row_idx + spot_row][cell_idx + spot_col]["name"] != "empty": continue
                        board[player][row_idx + spot_row][cell_idx + spot_col]["hit"] = True

def remove_all_hits(board):
    for player_board in board:
        for row in player_board:
            for cell in row:
                cell["hit"] = False

def convert_guess(guess):
    return ord(guess[0]) - 65, int(guess[1:]) - 1

def print_computer_vision(board, other_player, ships):
    cell_shippability = hard_computer_guesses(board, other_player, ships, return_shippability=True)

    probable_cells = []
    for cell in cell_shippability.values():
        if 0 <= cell <= 1000:
            probable_cells.append(cell)

    result = "    "
    for i in range(1, len(board[other_player][0]) + 1): 
        result += f"  {i}{' ' * (2 - len(str(i)))}"
    result += "\n"

    for row_idx, row in enumerate(board[other_player]):
        grid_line = "    " + "+---" * len(row) + "+\n"
        result += grid_line

        row_line = f" {chr(65 + row_idx)}  "
        
        for cell_idx, cell in enumerate(row):
            shippability = cell_shippability.get(to_cell(row_idx, cell_idx), 0)
            
            if shippability == -1:
                bg_color = [0, 0, 0]
                display_text = " X "
            elif shippability >= 1000:
                bg_color = [255, 255, 255]
                display_text = f"G{(shippability // 1000)}"
                display_text = f" {display_text} " if len(display_text) == 1 else f"{display_text} "
            else:  
                prob = max(probable_cells)
                if prob == 0: prob = 1
                ratio = shippability / prob

                if ratio < 0.55:
                    are = int(100 * (ratio * 1.5))
                    guh = 250
                else:
                    are = 200
                    if ratio > 0.95:
                        ratio = ratio ** 4
                        are = int(100 * ratio)
                    guh = int(200 * (1 - (ratio - 0.5) * 2))
                buh = 0
                bg_color = [are, guh, buh]
                
                display_text = str(shippability)
                if len(display_text) == 1:
                    display_text = f" {display_text} "
                elif len(display_text) == 2:
                    display_text = f" {display_text}"

            row_line += f"|\033[48;2;{bg_color[0]};{bg_color[1]};{bg_color[2]}m{display_text}\033[0m"
        
        row_line += "|\n"
        result += row_line

    result += "    " + "+---" * len(board[other_player][0]) + "+\n"
    return result
    
def print_board(board, player_num, player_turn):
    water_bg = [120, 200, 250]
    ship_bg = [100, 100, 100]
    black = "\033[38;2;0;0;0;48;2;"
    intersection = f"{black}{water_bg[0]};{water_bg[1]};{water_bg[2]}m+"
    player_board = board[player_num]

    result = "    "
    for i in range(1, len(player_board[0]) + 1): 
        result += f"  {i}{" " * (2 - len(str(i)))}"
    result += "\n"

    for row_idx, row in enumerate(player_board):
        grid_line = "    "
        for cell_idx, cell in enumerate(row):
            ship_info = cell["name"]
            is_ship = ship_info != "empty"

            same_ship_above = False
            ship_visible = False
            if is_ship:
                if player_num == player_turn or player_turn == 3:
                    ship_visible = True
                else:
                    ship_visible = False
                if row_idx > 0:
                    above_cell = player_board[row_idx - 1][cell_idx]
                    above_ship_info = above_cell["name"]
                    if above_ship_info != "empty" and above_ship_info == ship_info:
                        if ship_visible or (cell["hit"] and above_cell["hit"]):
                            same_ship_above = True

            line_bg = water_bg
            if same_ship_above:
                if not ship_visible and cell["hit"] and player_board[row_idx - 1][cell_idx]["hit"]:
                    line_bg = [175, 90, 90]
                else:
                    line_bg = ship_bg
            
            grid_line += f"{intersection}{black}{line_bg[0]};{line_bg[1]};{line_bg[2]}m---"
        
        grid_line += f"{intersection}\033[0m\n"
        result += grid_line

        row_line = f" {chr(65 + row_idx)}  "
        
        for cell_idx, cell in enumerate(row):
            ship_info = cell["name"]
            is_hit = cell["hit"]
            is_ship = ship_info != "empty"

            bg_color = water_bg
            character = " "
            ship_visible = False
            if is_ship:
                if player_num == player_turn or player_turn == 3 or True not in get_health(board[player_num], ship_info):
                    ship_visible = True
                else:
                    ship_visible = False

            if is_ship and (is_hit or ship_visible):
                bg_color = ship_bg
                if not ship_visible:
                    bg_color = [175, 90, 90]

            if is_hit:
                character = "X"

            same_ship_left = False
            if cell_idx > 0 and is_ship:
                left_cell = row[cell_idx - 1]
                left_ship_info = left_cell["name"]
                if left_ship_info != "empty" and left_ship_info == ship_info:
                    if ship_visible or (is_hit and left_cell["hit"]):
                        same_ship_left = True

            pipe_bg = water_bg
            if same_ship_left:
                if not ship_visible and is_hit and left_cell["hit"]:
                    pipe_bg = [175, 90, 90]
                else:
                    pipe_bg = ship_bg

            row_line += f"{black}{pipe_bg[0]};{pipe_bg[1]};{pipe_bg[2]}m|"
            row_line += f"\033[48;2;{bg_color[0]};{bg_color[1]};{bg_color[2]}m {character} "
        
        row_line += f"{black}{water_bg[0]};{water_bg[1]};{water_bg[2]}m|\033[0m"
        result += row_line + "\n"

    final_line = "    "
    for _ in range(len(player_board[0])):
        final_line += f"{black}{water_bg[0]};{water_bg[1]};{water_bg[2]}m+---"
    final_line += f"{black}{water_bg[0]};{water_bg[1]};{water_bg[2]}m+\033[0m\n"
    result += final_line

    return(result)

def place_ship(player, board, ship, cell, direction, tactical):
    if not check_direction(player, board, ship, cell, direction): return False
    row, col = convert_guess(cell)

    for i in range(ship["length"]):
        match direction.upper():
            case "UP":
                board[player][row - i][col]["name"] = ship["name"]
                board[player][row - i][col]["length"] = ship["length"]
            case "DOWN":
                board[player][row + i][col]["name"] = ship["name"]
                board[player][row + i][col]["length"]= ship["length"]
            case "LEFT":
                board[player][row][col - i]["name"] = ship["name"]
                board[player][row][col - i]["length"] = ship["length"]
            case "RIGHT":
                board[player][row][col + i]["name"] = ship["name"]
                board[player][row][col + i]["length"] = ship["length"]

    if tactical:
        tactical_obliteration(player, board, ship["name"])
                
    return True
        

def check_direction(player, board, ship, cell, direction, hypothetical=False):
    length = ship["length"]
    row, col = convert_guess(cell)
    
    match direction.upper():
        case "UP":
            if row - length + 1 < 0: 
                return False
            for i in range(length):
                if hypothetical: 
                    if board[player][row - i][col]["hit"]:
                        return False
                    else: continue
                if board[player][row - i][col]["name"] != "empty" or board[player][row - i][col]["hit"]:
                    return False
                    
        case "DOWN":
            if row + length > len(board[player]): 
                return False
            for i in range(length):
                if hypothetical: 
                    if board[player][row + i][col]["hit"]:
                        return False
                    else: continue
                if board[player][row + i][col]["name"] != "empty" or board[player][row + i][col]["hit"]:
                    return False
                    
        case "LEFT":
            if col - length + 1 < 0: 
                return False
            for i in range(length):
                if hypothetical: 
                    if board[player][row][col - i]["hit"]:
                        return False
                    else: continue
                if board[player][row][col - i]["name"] != "empty" or board[player][row][col - i]["hit"]:
                    return False
                    
        case "RIGHT":
            if col + length > len(board[player]): 
                return False
            for i in range(length):
                if hypothetical: 
                    if board[player][row][col + i]["hit"]:
                        return False
                    else: continue
                if board[player][row][col + i]["name"] != "empty" or board[player][row][col + i]["hit"]:
                    return False

    return True

def check_game_state(board, ships):
    game_over = [True, True]
    for player in range(2):
        for ship in ships:
            for segment in get_health(board[player], ship["name"]):
                if segment: game_over[player] = False

    return True in game_over

def medium_computer_guesses(board, player):
    potential_guesses = []
    for row in range(len(board[player])):
        for col in range(len(board[player][row])):
            if board[player][row][col]['name'] != 'empty':
                if board[player][row][col]['hit']:
                    direction = 'unknown'
                    sunk = True
                    segments_hit = 0
                    for segment in get_health(board[player], board[player][row][col]['name']):
                        if segment:
                            sunk = False
                        else:
                            segments_hit += 1
                    if not(sunk):
                        if segments_hit >= 2:
                            if row != 0:
                                if board[player][row-1][col]['hit'] and board[player][row-1][col]['name'] != 'empty':
                                    if board[player][row-1][col]['name'] == board[player][row][col]['name']:
                                        direction = 'vertical'
                            if row < len(board[0])-1:
                                if board[player][row+1][col]['hit'] and board[player][row+1][col]['name'] != 'empty':
                                    if board[player][row+1][col]['name'] == board[player][row][col]['name']:
                                        direction = 'vertical'
                            if col != 0:
                                if board[player][row][col-1]['hit'] and board[player][row][col-1]['name'] != 'empty':
                                    if board[player][row][col-1]['name'] == board[player][row][col]['name']:
                                        direction = 'horizontal'
                            if col < len(board[0][0])-1:
                                if board[player][row][col+1]['hit'] and board[player][row][col+1]['name'] != 'empty':
                                    if board[player][row][col+1]['name'] == board[player][row][col]['name']:
                                        direction = 'horizontal'
                        if row != 0 and direction != 'horizontal':
                            if not(board[player][row-1][col]['hit']) and (chr(65+row-1)+str(col+1)) not in potential_guesses:
                                potential_guesses.append(chr(65+row-1)+str(col+1))
                        if row < len(board[player])-1 and direction != 'horizontal':
                            if not(board[player][row+1][col]['hit']) and (chr(65+row+1)+str(col+1)) not in potential_guesses:
                                potential_guesses.append(chr(65+row+1)+str(col+1))
                        if col != 0 and direction != 'vertical':
                            if not(board[player][row][col-1]['hit']) and (chr(65+row)+str(col)) not in potential_guesses:
                                potential_guesses.append(chr(65+row)+str(col))
                        if col < len(board[0][0])-1 and direction != 'vertical':
                            if not(board[player][row][col+1]['hit']) and (chr(65+row)+str(col+2)) not in potential_guesses:
                                potential_guesses.append(chr(65+row)+str(col+2))
    if len(potential_guesses) > 0:
        return potential_guesses
    else:
        for row in range(len(board[player])):
            for col in range(len(board[player][0])):
                if not(board[player][row][col]['hit']) and (row+col) % 2 == 0:
                    potential_guesses.append(chr(65+row)+str(col+1))
        return potential_guesses
    
def place_random_ships(player_num, ships, board, tactical):
    player_grid = board[player_num]
    directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
    modifier = 0
    if tactical: modifier = 1
    for ship in ships:
        if len(player_grid[0]) - modifier <= ship['length'] >= len(player_grid) - modifier: 
            for segment in range(ship["length"]): ship["health"][segment] = False
            continue
        ship_placed = False

        while True:
            row = random.randint(0, len(board[0])-1)
            col = random.randint(0, len(board[0][0])-1)
            cell = to_cell(row, col)
            if board[player_num][row][col]['name'] == 'empty':
                possible_directions = []
                for direction in directions:
                    if check_direction(player_num, board, ship, cell, direction): 
                        possible_directions.append(direction)
                    
                if possible_directions:
                    direction = random.choice(possible_directions)
                    place_ship(player_num, board, ship, cell, direction, tactical)
                    ship_placed = True
                    break

        if not ship_placed:

            for row_idx, row in enumerate(board[player_num]):
                for cell_idx, cell in enumerate(row):
                    board[player_num][row_idx][cell_idx]["name"] = "empty" 
                    board[player_num][row_idx][cell_idx]["hit"] = False
            
            place_random_ships(player_num, ships, board, tactical)
            return 

def place_manual_ships(player_num, ships, board, tactical):
    directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
    player_grid = board[player_num]
    modifier = 0
    if tactical: modifier = 1
    for ship in ships:

        if len(player_grid[0]) - modifier <= ship["length"] >= len(player_grid) - modifier: 
            for segment in range(ship["length"]): ship["health"][segment] = False
            continue
        while True:
            possible_directions = []
            print(f"Player {player_num+1}:")
            print(print_board(board, player_num, player_num))
            location = input(f"Enter location to place {ship['name']} (length {ship['length']}): ").upper()
            if not validate_guess(board, location, 1, 1, num_players):
                print("Please enter a valid location on the board.")
                continue
            row, col = convert_guess(location)
            if player_grid[row][col]['name'] != 'empty':
                print("There is already a ship at this location.")
                continue
            for direction in directions:
                if check_direction(player_num, board, ship, location, direction):
                    possible_directions.append(direction)
            if len(possible_directions) == 0:
                print("Ship cannot fit at this location.")
                continue
            break
        while True:
            print(f"Possible directions: {possible_directions}")
            direction = collect_stringput("Enter direction to place the ship: ", possible_directions, case_sensitive=False)
            place_ship(player_num, board, ship, location, direction, tactical)
            break
    print("\n" * 40)
    if player_num == 1:
        input(f"Player 1, press enter to see your board.")

def create_board(size):
    board = []
    for i in range(2):
        player_grid = []
        for row in range(size):
            grid_row = []
            for col in range(size):
                grid_row.append({
                    'name': 'empty',
                    'hit': False,
                    "length": 0
                })
            player_grid.append(grid_row)
        board.append(player_grid)
    return board

def validate_guess(board, guess, current_player, other_player, num_players):
    try:
        row, col = convert_guess(guess)
    except:
        if current_player == 0:
            print("Please enter a valid location on the board.")
        return False
    if row < 0 or row >= len(board[0]) or col < 0 or col >= len(board[0][0]):
        if current_player == 0:
            print("Please enter a valid location on the board.")
        return False
    elif not board[other_player][row][col]['hit']:
        return True
    if current_player == 0 and num_players > 0:
        print("You have already fired on this cell.")
    return False

def reverse_player(player):
    if player == 0:
        return 1
    return 0

def computer_turn(board, current_player, difficulty, debug):
    if difficulty == "hard":
        if debug: print_horizontal(print_computer_vision(board, 0, ships), print_computer_vision(board, 1, ships), 5)
        computer_guesses = hard_computer_guesses(board, other_player, ships)
        guess = computer_guesses[random.randint(0, len(computer_guesses) - 1)]
    elif difficulty == 'medium':
        guess = medium_computer_guesses(board, other_player)[random.randint(0,len(medium_computer_guesses(board, other_player)) - 1)]
    else:
        while(True):
            row_guess = random.randint(0, len(board[0])-1)
            col_guess = random.randint(0, len(board[0][0])-1)
            guess = to_cell(row_guess, col_guess)
            if validate_guess(board, guess, current_player, other_player, num_players):
                break
    return guess

def manual_turn(board, current_player):
    print_horizontal(print_board(board, 0, player_turn), print_board(board, 1, player_turn), 5)
    guess = input("Which cell would you like to fire on? (e.g: A1, C3, D4): ").upper()
    while not validate_guess(board, guess, current_player, other_player, num_players):
        guess = input("Which cell would you like to fire on? (e.g: A1, C3, D4): ").upper()
    return guess

if __name__ == "__main__":
    player_accuracies = []
    num_players = collect_intput("How many players? (max 2): ", 2, 0)
    grid_size = 10 #collect_intput("Enter grid size (4-10): ", 10, 4)
    difficulty_1 = ''
    difficulty_2 = ''

    if num_players == 1:
        difficulty_2 = collect_stringput("Select difficulty level of computer opponent (easy/medium/hard): ", ['easy', 'medium', "hard"], case_sensitive=False).lower()
    elif num_players == 0:
        difficulty_1 = collect_stringput("Select difficulty for Player 1 (easy/medium/hard): ", ['easy', 'medium', "hard"], case_sensitive=False).lower()
        difficulty_2 = collect_stringput("Select difficulty for Player 2 (easy/medium/hard): ", ['easy', 'medium', "hard"], case_sensitive=False).lower()
    if num_players == 1:  
        placement_method_1 = collect_stringput("Player 1: Place ships randomly or manually? (r/m): ", ['r', 'm'], case_sensitive=False).lower()
        placement_method_2 = 'r'
    elif num_players == 2:
        placement_method_1 = collect_stringput("Player 1: Place ships randomly or manually? (r/m): ", ['r', 'm'], case_sensitive=False).lower()
        placement_method_2 = collect_stringput("Player 2: Place ships randomly or manually? (r/m): ", ['r', 'm'], case_sensitive=False).lower()
    else:
        placement_method_1 = 'r'
        placement_method_2 = 'r'
    blitz = collect_stringput("Play in blitz mode? (extra turn on hits) (y/n): ", ["y", "n"], case_sensitive=False)
    tactical_input = "n" if grid_size < 8 else collect_stringput("Play with Convention on the International Regulations for Preventing Collisions at Sea approved ship placement? (y/n): ", ["y", "n"], case_sensitive=False)
    tactical = True if tactical_input == "y" else False
    debug = True if (difficulty_1 == "hard" or difficulty_2 == "hard") and collect_stringput("Debug mode? (y/n): ", ["y", "n"], case_sensitive=False) == "y" else False
    player_turn = 0
    board = create_board(grid_size)

    ships = [
        {'name': 'carrier', 'length': 5},
        {'name': 'battleship', 'length': 4},
        {'name': 'destroyer', 'length': 3}, 
        {'name': 'submarine', 'length': 3},
        {'name': 'patrol boat', 'length': 2},
    ]

    if placement_method_1 == 'r':
        place_random_ships(0, ships, board, tactical)
    else:
        place_manual_ships(0, ships, board, tactical)

    if placement_method_2 == 'r':
        place_random_ships(1, ships, board, tactical)
    else:
        place_manual_ships(1, ships, board, tactical)

    remove_all_hits(board)
    
    while (True):
        current_player = player_turn
        other_player = reverse_player(player_turn)
        print("\n" * 40)
        print(f"=== Player {current_player + 1}'s Turn! ===")
        if num_players == 2 or (num_players == 1 and player_turn == 0):
            guess = manual_turn(board, current_player)
            computer_choices = hard_computer_guesses(board, other_player, ships, True)
            player_choice_ranking = get_bracket_ranking(guess, bracket_dict_values(computer_choices))
            print(f"Your move was one of the {num_end(player_choice_ranking)}-best moves.")
        else:
            if current_player == 0:
                difficulty = difficulty_1
            else:
                difficulty = difficulty_2
            guess = computer_turn(board, current_player, difficulty, debug)
        hit = shoot(other_player, guess, board, tactical, current_player)

        if check_game_state(board, ships):
            print("GAME OVER!!!")
            print(f"Player {current_player + 1} wins!!")
            break
        if num_players != 1:
            print_horizontal(print_board(board, 0, current_player), print_board(board, 1, current_player), 5)
        elif num_players == 0:
            print_horizontal(print_board(board, 0, 0), print_board(board, 1, 1), 5)
        else:
            print_horizontal(print_board(board, 0, 0), print_board(board, 1, 0), 5)
        if player_turn == 1:
            evaluation = (sum(value for value in hard_computer_guesses(board, 0, ships, True).values() if -1 < value < 1000) - sum(value for value in hard_computer_guesses(board, 1, ships, True).values() if -1 < value < 1000)) / (grid_size*grid_size)
            color = "\033[92m" if evaluation >= 0 else "\033[91m"
            print(f"COMPUTER EVALUATION: {color}{abs(evaluation):.2f}\033[0m")
        input(f"Press enter to continue.")

        if (blitz != "y" or not hit): 
            player_turn = reverse_player(player_turn)
            print("\n" * 40)
            if num_players == 2:
                input(f"Player {other_player+1}, press enter to see your board.") 
                       

    print_horizontal(print_board(board, 0, 3), print_board(board, 1, 3), 5)