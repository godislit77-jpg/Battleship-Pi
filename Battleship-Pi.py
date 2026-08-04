import math
import time
import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def board(size):
    board = []
    for _ in range(size):
        rows = []
        for _ in range(size):
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

def placeAdjacentShips(shipLocations, row, col, axis, givenShipDict):
    adjacentSpacesTried = 0
    index = None
    if axis == "row":
        index = 0
        axisValue = row
    else:
        index = 1
        axisValue = col

    directionToMakeAdjacentSpace = random.choice([1, -1])
    while adjacentSpacesTried < 2:
        repeatedSpace = False
        maxAxisValue = None
        minAxisValue = None
        for location in shipLocations:
            if maxAxisValue == None:
                minAxisValue = maxAxisValue = location[index]
            elif location[index] == None:
                continue
            elif location[index] > maxAxisValue:
                maxAxisValue = location[index]
            elif location[index] < minAxisValue:
                minAxisValue = location[index]
        if adjacentSpacesTried != 0:
            if directionToMakeAdjacentSpace == 1:
                directionToMakeAdjacentSpace = -1
            if directionToMakeAdjacentSpace == -1:
                directionToMakeAdjacentSpace = 1

        if directionToMakeAdjacentSpace == 1:
            axisValue = maxAxisValue + 1
        else:
            axisValue = minAxisValue - 1
        adjacentSpacesTried += 1
        if axisValue < 0 or axisValue > 9:
                continue
        if axis == "col":
            for ships in givenShipDict:
                if [row, axisValue] in givenShipDict[ships]["location"]:
                    repeatedSpace = True
                    break
        else:
            for ships in givenShipDict:
                if [axisValue, col] in givenShipDict[ships]["location"]:
                    repeatedSpace = True
                    break
        if repeatedSpace:
            continue
        return axisValue
    return False


def ship_placement(board, placementProcess, givenShipDict):
    for ship in givenShipDict.items():
        spacesPlaced = 0
        shipLength = ship[1]['length']
        orientation = random.choice(["horizontal", "vertical"])
        row = None
        col = None
        check2 = True
        while spacesPlaced < shipLength:

            spaceNotOpen = True

            while spaceNotOpen:
                spaceNotOpen = False
                if spacesPlaced == 0 and placementProcess == "randomly":
                    row = random.randint(0,len(board)-1)
                    col = random.randint(0,len(board)-1)
                elif spacesPlaced > 0 and placementProcess == "randomly":
                    if orientation == "vertical":
                        row = placeAdjacentShips(ship[1]["location"], row, col, "row", givenShipDict)
                    elif orientation == "horizontal":
                        col = placeAdjacentShips(ship[1]["location"], row, col, "col", givenShipDict)
                    if str(row) == "False" or str(col) == "False":
                        spaceNotOpen = True
                        spacesPlaced = 0
                        ship[1]["location"] = []
                        for _ in range(ship[1]["length"]):
                            ship[1]['location'].append([None, None])
                        continue

                elif placementProcess == "manually":
                    check = True
                    while check:
                        while check2:
                            orientation = input(f"Would you like to place your {ship[0]} horizontal or vertical: ")
                            if orientation not in ["horizontal","vertical"]:
                                print("Please Put a Valid Input")
                            else:
                                check2 = False
                        spaceInput = input(f"Please enter cell eg (A1,B2,C3) for {ship[0]}: ").upper()
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
                                for shipss in givenShipDict:
                                    for location in givenShipDict[shipss]["location"]:
                                        if location[0] == None:
                                            continue
                                        elif (location[0] == row and abs(location[1] - col) == 1 and orientation == "horizontal"):
                                            check = False
                                        elif (abs(location[0] - row) == 1 and location[1] == col and orientation == "vertical"):                                           
                                            check = False
                                if check:
                                    print(f"Coordinates of the same ship must be adjacent and {orientation}")

                for ships in givenShipDict:
                    if [row, col] in givenShipDict[ships]["location"]:
                        spaceNotOpen = True
                if spaceNotOpen == True and placementProcess == "manually":
                    print("Space has already been used")

            ship[1]['location'][spacesPlaced] = [row, col]
            spacesPlaced += 1

def playerDisplay(playerBoard,playerDict):
    for ships in playerDict:
        for i in range(len(playerDict[ships]['location'])):
            row = playerDict[ships]['location'][i][0]
            col = playerDict[ships]['location'][i][1]
            if ships == "destroyer":
                playerBoard[row][col] = "S"
            elif ships == "submarine":
                playerBoard[row][col] = "S"
                playerBoard[row][col] = "S"
            elif ships == "cruiser":
                playerBoard[row][col] = "S"
            elif ships == "battleship":
                playerBoard[row][col] = "S"
            elif ships == "carrier":
                playerBoard[row][col] = "S"


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


def printboard(board,turn):
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

    if turn == 1:
        
        y = 3
        for row in board:
            x = 4
            for cell in row:
                if cell == '.':
                    frameCanvas.SetPixel(x, y, 0, 0, 200)
                elif cell == 'H':
                    frameCanvas.SetPixel(x, y, 200, 0, 0)
                elif cell == 'S':
                    frameCanvas.SetPixel(x, y, 155, 155, 155)
                elif cell == 'M':
                    frameCanvas.SetPixel(x, y, 0, 128, 128)
                x += 1
            y += 1
        
    else:

        y = 3
        for row in board:
            x = 18
            for cell in row:
                if cell == '.':
                    frameCanvas.SetPixel(x, y, 0, 0, 200)
                elif cell == 'H':
                    frameCanvas.SetPixel(x, y, 200, 0, 0) 
                elif cell == 'M':
                    frameCanvas.SetPixel(x, y, 0, 128, 128)                               
                x += 1
        y += 1

    frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
    
def hitShip(turnNumber, rowIndex, columnIndex):
    if turnNumber % 2 == 1:
        currentPlayerDict = computerShips
        currentBoard = computerBoard
        turn = 0
        print("YOUR TURN")
    else:
        currentPlayerDict = playerShips
        currentBoard = playerBoard
        turn = 1
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
            currentBoard[rowIndex][columnIndex] = "H"
            if numberOfTimesHitShipPrint == 0:
                print("SHIP HIT")
                numberOfTimesHitShipPrint += 1
            if not currentPlayerDict[ship]["location"]:
                print(f"{ship} SUNK")
            printboard(currentBoard)
            return
        elif hitShip == False and numberOfShipsChecked == len(currentPlayerDict):
            currentBoard[rowIndex][columnIndex] = "X"
            print("SHIP MISSED")
        numberOfShipsChecked += 1
    printboard(currentBoard,turn)


if __name__ == '__main__':

    # ==========================================================
    # RGB MATRIX CONFIGURATION
    # ==========================================================
    matrixOptions = RGBMatrixOptions()
    matrixOptions.rows = 16
    matrixOptions.cols = 32
    matrixOptions.chain_length = 1
    matrixOptions.parallel = 1
    matrixOptions.hardware_mapping = "adafruit-hat"
    matrixOptions.gpio_slowdown = 4
    matrixOptions.disable_hardware_pulsing = True

    matrixDisplay = RGBMatrix(options=matrixOptions)
    frameCanvas = matrixDisplay.CreateFrameCanvas()

    screenWidth = matrixOptions.cols
    screenHeight = matrixOptions.rows





    for i in range(3):
        for x in range(0,screenWidth):
            frameCanvas.SetPixel(x,i,50,50,100)
        for x in range(0,screenWidth):
            frameCanvas.SetPixel(x,15 - i,50,50,100)
    for i in range(4):
        for y in range(0,screenHeight):
            frameCanvas.SetPixel(i,y,50,50,100)
        for y in range(0,screenHeight):
                frameCanvas.SetPixel(31 - i,y,50,50,100)
        for y in range(0,screenHeight):
            frameCanvas.SetPixel(14 + i,y,50,50,100)

    frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
        

    

    # Dictionary of ships and their locations

    playerShips = {
        "carrier" : {
            "length" : 5,
            "location" : [[None, None], [None, None], [None, None], [None, None], [None, None]]
        },

        "destroyer" : {
            "length" : 2,
            "location" :[[None, None], [None, None]] 
                },
        "cruiser" : {
                "length" : 3,
                "location" : [[None, None], [None, None], [None, None]]
                },
        "submarine" : {
                        "length" : 3,
                        "location" : [[None, None], [None, None], [None, None]]
                        },
        "battleship" : {
                        "length" : 4,
                        "location" : [[None, None], [None, None], [None, None], [None, None]]
                        },
    }

    computerShips = {
        "carrier" : {
            "length" : 5,
            "location" : [[None, None], [None, None], [None, None], [None, None], [None, None]]
        },

        "destroyer" : {
            "length" : 2,
            "location" :[[None, None], [None, None]] 
                },
        "cruiser" : {
                "length" : 3,
                "location" : [[None, None], [None, None], [None, None]]
                },
        "submarine" : {
                        "length" : 3,
                        "location" : [[None, None], [None, None], [None, None]]
                        },
        "battleship" : {
                        "length" : 4,
                        "location" : [[None, None], [None, None], [None, None], [None, None]]
                        },
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

    sizeOfBoard = 10
    playerBoard = board(sizeOfBoard)
    computerBoard = board(sizeOfBoard)

    # Loops through each ship in a given dictionary
    # Places ships on the board
    ship_placement(playerBoard, userShipPlacementProcess, playerShips)
    playerDisplay(playerBoard,playerShips)
    ship_placement(computerBoard, "randomly", computerShips)

    winner = None
    noWinner = True
    turnNumber = 1
    while noWinner:
        try:
            time.sleep(1 / 60)
        except KeyboardInterrupt:
            print("\nExiting cleanly...")
            matrixDisplay.Clear()
            break
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
                if validate_input(f"{chr(columnIndex+65)}{rowIndex+1}") == False and computerBoard[rowIndex][columnIndex] == ".": 
                    guessIsOffOfBoard = False
                else:
                    continue
            hitShip(turnNumber, rowIndex, columnIndex)
            turnNumber +=1 

        winner,noWinner = win_checker(playerShips, computerShips)

    print("GAME OVER")
    print(f"WINNER: {winner}")