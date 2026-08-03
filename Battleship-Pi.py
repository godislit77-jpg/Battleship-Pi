import random

def board(size):
    board = []
    for i in range(size):
        rows = []
        for i in range(size):
            cells = "."
            rows.append(cells)
        board.append(rows)
    return board

def validate_input(cell_input):
    try:
        if cell_input[0].isalpha() and ord(cell_input[0])-65 >= 0 and ord(cell_input[0])-65 < sizeOfBoard:
            if int(cell_input[1:]):
                if int(cell_input[1:]) <= sizeOfBoard and int(cell_input[1:]) > 0:
                    return False
    except:
        return True
    return True

def ship_placement(board, placementProcess, givenShipDict):
    for ship in givenShipDict:
        spacesPlaced = 0
        shipLength = givenShipDict[ship]['length']
        orientation = random.choice(["horizontal", "vertical"])
        row = None
        col = None
        while spacesPlaced < shipLength:

            spaceNotOpen = True

            while spaceNotOpen:
                spaceNotOpen = False
                if spacesPlaced == 0 and placementProcess == "randomly":
                    row = random.randint(0,len(board)-1)
                    col = random.randint(0,len(board)-1)
                elif spacesPlaced > 0 and placementProcess == "randomly":
                    if orientation == "vertical":
                        while True:
                            row = row + random.choice([1, -1])
                            if row > len(board)-1:
                                row -= 1
                                continue
                            elif row < 0: 
                                row += 1
                                continue
                            if row <= len(board)-1 and row >= 0:
                                    break
                    elif orientation == "horizontal":
                        while True:
                            col = col + random.choice([1, -1])
                            if col > len(board):
                                col -= 1
                                continue
                            elif col < 0: 
                                col += 1
                                continue
                            if col < len(board) and col >= 0:
                                break
                elif placementProcess == "manually":
                    check = True
                    while check:
                        spaceInput = input(f"Please enter cell eg (A1,B2,C3) for {ship}: ")
                        spaceInput = input(f"Please enter cell eg (A1,B2,C3) for {ship}: ").upper()
                        check = validate_input(spaceInput)
                        if check == True:
                            print("Please enter a valid coordinate")
                            continue
                        col = ord(spaceInput[0]) - 65
                        row = int(spaceInput[1:])-1
                        if check == True:
                            print("Please enter a valid coordinate")
                        if spacesPlaced > 0:
                                check = True
                                for location in givenShipDict[ship]["location"]:
                                    if location[0] == None:
                                        continue
                                    elif (location[0] == row and abs(location[1] - col) == 1) or (abs(location[0] - row) == 1 and location[1] == col):                                           
                                        check = False
                                if check:
                                    print("Coordinates of the same ship must be adjacent")

                for ships in givenShipDict:
                    if [row, col] in givenShipDict[ships]["location"]:
                        spaceNotOpen = True
                if spaceNotOpen == True:
                    print("Space has already been used")

            givenShipDict[ship]["location"][spacesPlaced] = [row, col]
            spacesPlaced += 1


def win_checker(playerShips,computerShips):
    sunk_ships = 0
    for ship in playerShips:
        if not playerShips[ship]['location']:
            sunk_ships += 1
    if sunk_ships == len(playerShips):
        return "computer",False
    sunk_ships = 0
    for ship in computerShips:
        if not computerShips[ship]['location']:
            sunk_ships += 1
        if sunk_ships == len(computerShips):
            return "player",False
    return None,True 


def printboard(board):
    columns = [chr(65+int(colNumber)) for colNumber in range(sizeOfBoard)]
    print("\t",end="")
    for x in columns:
        print(f"{x} \t",end="")
    print("")
    index = 0
    for rows in board:
        index += 1
        print(str(index)+"\t",end="")
        for cells in rows:
            print(f"{cells} \t",end="")
        print("\t")




def hitShip(turnNumber, rowIndex, columnIndex):
    if turnNumber % 2 == 1:
        currentPlayerDict = computerShips
        currentBoard = computerBoard
        print("YOUR TURN")
    else:

        currentPlayerDict = playerShips
        currentBoard = playerBoard
        print("COMPUTER'S TURN")
        print(f"COMPUTER GUESSED: {chr(columnIndex +65)}{rowIndex + 1}")
    hitShip = False
    numberOfShipsChecked = 1
    numberOfTimesHitShipPrint = 0
    for ship in currentPlayerDict:
        if [rowIndex, columnIndex] in currentPlayerDict[ship]["location"]:
            currentPlayerDict[ship]["location"].remove([rowIndex,columnIndex])
            hitShip = True
        if hitShip:
            currentBoard[rowIndex][columnIndex] = "💥"
            if numberOfTimesHitShipPrint == 0:
                print("SHIP HIT")
                numberOfTimesHitShipPrint += 1
            if not currentPlayerDict[ship]["location"]:
                print(f"{ship} SUNK")
        elif hitShip == False and numberOfShipsChecked == len(currentPlayerDict):
            currentBoard[rowIndex][columnIndex] = "X"
            print("SHIP MISSED")
        numberOfShipsChecked += 1
    printboard(currentBoard)


if __name__ == '__main__':

    # Dictionary of ships and their locations

    playerShips = {
        "dinghy" : {
            "length" : 1,
            "location" :[[None, None]] 
        },
        "destroyer" : {
            "length" : 2,
            "location" :[[None, None], [None, None]] 
                }
    }

    computerShips = {
        "dinghy" : {
            "length" : 1,
            "location" :[[None, None]] 
        },
        "destroyer" : {
            "length" : 2,
            "location" :[[None, None], [None, None]] 
                }
    }

    # Asks if player wants to place ships manually or automatically
    shipPlacementProcessBoolean = True
    while shipPlacementProcessBoolean:
        userShipPlacementProcess = input("Would you like to place the ships manually or randomly: ").lower().strip()
        if userShipPlacementProcess == "manually" or userShipPlacementProcess == "randomly":
            shipPlacementProcessBoolean = False
        else:
            print("Please enter \"manually\" or \"randomly\"")

    # Asks player for the size of the board and creates boards

    playerBoard = None
    computerBoard = None

    invalidSizeOfBoard = True

    while invalidSizeOfBoard:
        try:
            sizeOfBoard = int(input("Enter size of board (4-10): "))
            if sizeOfBoard < 4 or sizeOfBoard > 10:
                print("Please only enter numbers in the range 4-10")
                continue
            playerBoard = board(sizeOfBoard)
            computerBoard = board(sizeOfBoard)
            invalidSizeOfBoard = False

        except ValueError:
            print("Please only enter integers")

    # Loops through each ship in a given dictionary
    # Places ships on the board
    ship_placement(playerBoard, userShipPlacementProcess, playerShips)
    ship_placement(computerBoard, "randomly", computerShips)

    winner = None
    noWinner = True
    turnNumber = 1
    while noWinner:
        columnIndex = None
        rowIndex = None
        guessIsOffOfBoard = True
        validating = True
        while guessIsOffOfBoard:
            if turnNumber % 2 == 1:
                while validating:
                    try:
                        guess = input("Guess where the ship is: ").strip().upper()
                        columnIndex = int(ord(guess[0]) - 65)
                        rowIndex = int(guess[1:])-1
                    except:
                        print("Invalid Guess")
                    if validate_input(guess) == True:
                        print("Please enter a valid location")
                    else:
                        if computerBoard[rowIndex][columnIndex] != ".":
                            print("You already guessed this space")
                        else:
                            guessIsOffOfBoard = False
                            validating = False
            else:
                columnIndex = random.randint(0, len(computerBoard) - 1)
                rowIndex = random.randint(0, len(computerBoard) - 1)
                if validate_input(f"{chr(columnIndex+65)}{rowIndex+1}") == False and playerBoard[rowIndex][columnIndex] == ".": 
                    guessIsOffOfBoard = False
                else:
                    continue
            hitShip(turnNumber, rowIndex, columnIndex)
            turnNumber +=1 

        winner,noWinner = win_checker(playerShips, computerShips)

    print("GAME OVER")
    print(f"WINNER: {winner}")