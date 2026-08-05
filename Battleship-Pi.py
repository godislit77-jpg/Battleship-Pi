import math
import time
import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions

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


def win_checker(player1Ships,player2Ships):
    sunk_ships = 0
    for ship in player1Ships:
        if player1Ships[ship]["health"] == 0:
            sunk_ships += 1
    if sunk_ships == len(player1Ships):
        if mode == 's':
            return "computer",False
        else:
            return "Player 2",False
    sunk_ships = 0
    for ship in player2Ships:
        if player2Ships[ship]["health"] == 0:
            sunk_ships += 1
        if sunk_ships == len(player2Ships):
            if mode == 's':
                return "player",False
            else:
                return "Player 1",False
    return None,True 


def printboard(board,turn,frameCanvas):
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
        
        y = 3
        for row in board:
            x = 4
            for cell in row:
                if cell == '.':
                    frameCanvas.SetPixel(x, y, 0, 0, 200)
                elif cell == 'H':
                    frameCanvas.SetPixel(x, y, 255, 165, 0)
                elif cell == 'S':
                    frameCanvas.SetPixel(x, y, 155, 155, 155)
                elif cell == 'X':
                    frameCanvas.SetPixel(x, y, 0, 128, 128)
                elif cell == "s":
                    frameCanvas.SetPixel(x, y,200,0,0)
                x += 1
            y += 1
        
    else:
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

        y = 3
        for com_row in board:
            x = 18
            for cells in com_row:
                if cells == '.':
                    frameCanvas.SetPixel(x, y, 0, 0, 200)
                elif cells == 'H':
                    frameCanvas.SetPixel(x, y, 255, 165, 0) 
                elif cells == 'X':
                    frameCanvas.SetPixel(x, y, 0, 128, 128) 
                elif cells == "s":
                    frameCanvas.SetPixel(x, y,200,0,0)                              
                x += 1
            y += 1

    frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
    
def hitShip(turnNumber, rowIndex, columnIndex,frameCanvas):
    if turnNumber % 2 == 1:
        currentPlayerDict = player2Ships
        currentBoard = player2Board
        turn = 0
        if mode == 's':
            print("YOUR TURN")
        else:
            print("PLAYER 1'S TURN")
    else:
        currentPlayerDict = player1Ships
        currentBoard = player1Board
        turn = 1
        if mode == 's':
            print("COMPUTER'S TURN")
            print(f"COMPUTER GUESSED: {chr(columnIndex +65)}{rowIndex + 1}")
        else:
            print("PLAYER 2'S TURN")
    hitShip = False
    numberOfShipsChecked = 1
    numberOfTimesHitShipPrint = 0
    for ship in currentPlayerDict:
        if [rowIndex, columnIndex] in currentPlayerDict[ship]["location"]:
            currentPlayerDict[ship]["health"] -= 1
            hitShip = True
        if hitShip:
            currentBoard[rowIndex][columnIndex] = "H"
            if numberOfTimesHitShipPrint == 0:
                print("SHIP HIT")
                numberOfTimesHitShipPrint += 1
            if currentPlayerDict[ship]["health"] == 0:
                print(f"{ship} SUNK")
                for location in currentPlayerDict[ship]["location"]:
                    currentBoard[location[0]][location[1]] = "s"
            printboard(currentBoard,turn,frameCanvas)
            return
        elif hitShip == False and numberOfShipsChecked == len(currentPlayerDict):
            currentBoard[rowIndex][columnIndex] = "X"
            print("SHIP MISSED")
        numberOfShipsChecked += 1
    printboard(currentBoard,turn,frameCanvas)


if __name__ == '__main__':        
    # Dictionary of ships and their locations

    player1Ships = {
        "carrier" : {
            "length" : 5,
            "health":5,
            "location" : [[None, None], [None, None], [None, None], [None, None], [None, None]]
        },

        "destroyer" : {
            "length" : 2,
            "health":2,
            "location" :[[None, None], [None, None]] 
                },
        "cruiser" : {
                "length" : 3,
                "health":3,
                "location" : [[None, None], [None, None], [None, None]]
                },
        "submarine" : {
                        "length" : 3,
                        "health":3,
                        "location" : [[None, None], [None, None], [None, None]]
                        },
        "battleship" : {
                        "length" : 4,
                        "health":4,
                        "location" : [[None, None], [None, None], [None, None], [None, None]]
                        },
    }

    player2Ships = {
        "carrier" : {
            "length" : 5,
            "health":5,
            "location" : [[None, None], [None, None], [None, None], [None, None], [None, None]]
        },

        "destroyer" : {
            "length" : 2,
            "health":2,
            "location" :[[None, None], [None, None]] 
                },
        "cruiser" : {
                "length" : 3,
                "health":3,
                "location" : [[None, None], [None, None], [None, None]]
                },
        "submarine" : {
                        "length" : 3,
                        "health":3,
                        "location" : [[None, None], [None, None], [None, None]]
                        },
        "battleship" : {
                        "length" : 4,
                        "health":4,
                        "location" : [[None, None], [None, None], [None, None], [None, None]]
                        },
    }

    mode = input("Single or Multiplayer mode? (s/m): ").lower()
    while mode != 's' or mode != 'm':
        mode = input("Please select 's' or 'm': ").lower()


    # Asks if player wants to place ships manually or automatically
    shipPlacementProcessBoolean1 = True
    while shipPlacementProcessBoolean1:
        player1ShipPlacementProcess = input("Would you like to place the ships manually or randomly: ").lower().strip()
        if player1ShipPlacementProcess == "manually" or player1ShipPlacementProcess == "randomly":
            shipPlacementProcessBoolean1 = False
        else:
            print("Please enter \"manually\" or \"randomly\"")

    if mode == 's':
        player2ShipPlacementProcess = 'randomly'
    else:
        shipPlacementProcessBoolean2 = True
        while shipPlacementProcessBoolean2:
            player2ShipPlacementProcess = input("Would you like to place the ships manually or randomly: ").lower().strip()
            if player2ShipPlacementProcess == "manually" or player2ShipPlacementProcess == "randomly":
                shipPlacementProcessBoolean2 = False
            else:
                print("Please enter \"manually\" or \"randomly\"")

    # Asks player for the size of the board and creates boards

    player1Board = None
    player2Board = None

    sizeOfBoard = 10
    player1Board = board(sizeOfBoard)
    player2Board = board(sizeOfBoard)

    # Loops through each ship in a given dictionary
    # Places ships on the board
    ship_placement(player1Board, player1ShipPlacementProcess, player1Ships)
    ship_placement(player2Board, player2ShipPlacementProcess, player2Ships)
    if mode == 's':
        playerDisplay(player1Board,player1Ships)
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
            if turnNumber % 2 == 1 or mode == 'm':
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
                        if turnNumber % 2 == 1:
                            if player2Board[rowIndex][columnIndex] != ".":
                                print("You already guessed this space")
                            else:
                                guessIsOffOfBoard = False
                                validating = False
                        else:
                            if player1Board[rowIndex][columnIndex] != ".":
                                print("You already guessed this space")
                            else:
                                guessIsOffOfBoard = False
                                validating = False                           
            elif mode == 's':
                columnIndex = random.randint(0, len(player2Board) - 1)
                rowIndex = random.randint(0, len(player2Board) - 1)
                if validate_input(f"{chr(columnIndex+65)}{rowIndex+1}") == False and player1Board[rowIndex][columnIndex] == "." or player1Board[rowIndex][columnIndex] == "S": 
                    guessIsOffOfBoard = False
                else:
                    continue
            
            hitShip(turnNumber, rowIndex, columnIndex,frameCanvas)
            turnNumber +=1 

        winner,noWinner = win_checker(player1Ships, player2Ships)

    print("GAME OVER")
    print(f"WINNER: {winner}")
    for i in range(10):
        if winner == "player":
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
            
            y = 3
            for row in player1Board:
                x = 4
                for cell in row:
                    frameCanvas.SetPixel(x,y,0,200,0)
                    x += 1
                y += 1
                
            y = 3
            for row in player2Board:
                x = 18
                for cell in row:
                    frameCanvas.SetPixel(x,y,200,0,0)
                    x += 1
                y += 1
            time.sleep(0.5)
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
            
            y = 3
            for row in player1Board:
                x = 4
                for cell in row:
                    frameCanvas.SetPixel(x,y,0,0,0)
                    x += 1
                y += 1
            
            y = 3
            for row in player2Board:
                x = 18
                for cell in row:
                    frameCanvas.SetPixel(x,y,0,0,0)
                    x += 1
                y += 1
            frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
            time.sleep(0.5)
        else:
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
                
                y = 3
                for com_row in player2Board:
                    x = 18
                    for cells in com_row:
                        frameCanvas.SetPixel(x,y,0,200,0)                             
                        x += 1
                    y += 1

                y = 3
                for row in player1Board:
                    x = 4
                    for cell in row:
                        frameCanvas.SetPixel(x,y,200,0,0)
                        x += 1
                    y += 1
                time.sleep(0.5)
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
                
                y = 3
                for com_row in player2Board:
                    x = 18
                    for cells in com_row:
                        frameCanvas.SetPixel(x,y,0,0,0)                             
                        x += 1
                    y += 1
                
                y = 3
                for row in player1Board:
                    x = 4
                    for cell in row:
                        frameCanvas.SetPixel(x,y,0,0,0)
                        x += 1
                    y += 1
                frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
                time.sleep(0.5)
        frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)