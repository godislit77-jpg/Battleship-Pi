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

battleshipTitle = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,2],[1,4],[2,1],[2,3],[4,1],
                   [4,2],[4,3],[4,4],[5,0],[5,2],[6,1],[6,2],[6,3],[6,4],
                   [8,0],[9,0],[9,1],[9,2],[9,3],[9,4],[10,0],[12,0],[13,0],
                   [13,1],[13,2],[13,3],[13,4],[14,0],[16,0],[16,1],[16,2],
                   [16,3],[16,4],[17,4],[18,4],[20,0],[20,1],[20,2],
                   [20,3],[20,4],[21,0],[21,2],[21,4],[23,0],[23,1],[23,2],
                   [23,4],[24,0],[24,2],[24,4],[25,0],[25,2],[25,3],[25,4],
                   [27,0],[27,1],[27,2],[27,3],[27,4],[28,2],[29,0],[29,1],
                   [29,2],[29,3],[29,4],[31,0],[31,1],[31,2],[31,3],[31,4],
                   [33,0],[33,1],[33,2],[33,3],[33,4],[34,0],[34,2],[35,1]]

shipAnimation = [[7,31],[8,31],[6,32],[7,32],[8,32],[9,32],[6,33],[7,33],[8,33],
                 [9,33],[10,33],[6,34],[7,34],[8,34],[9,34],[10,34],[5,35],
                 [6,35],[7,35],[8,35],[9,35],[10,35],[5,36],[7,36],[8,36],[9,36],
                 [10,36],[5,37],[6,37],[7,37],[8,37],[9,37],[10,37],[5,38],[6,38],
                 [7,38],[8,38],[9,38],[10,38],[7,39],[8,39],[9,39],[10,39],[7,40],
                 [8,40],[9,40],[7,41],[8,41]]
shipAnimationLast = [[7,31],[8,31],[6,32],[7,32],[8,32],[9,32],[6,33],[7,33],[8,33],
                 [9,33],[10,33],[6,34],[7,34],[8,34],[9,34],[10,34],[5,35],
                 [6,35],[7,35],[8,35],[9,35],[10,35],[5,36],[7,36],[8,36],[9,36],
                 [10,36],[5,37],[6,37],[7,37],[8,37],[9,37],[10,37],[5,38],[6,38],
                 [7,38],[8,38],[9,38],[10,38],[7,39],[8,39],[9,39],[10,39],[7,40],
                 [8,40],[9,40],[7,41],[8,41]]
wave1 = [[10,0],[10,1],[11,2],[12,3],[12,4],[11,5],[10,6],[10,7],[11,8],[12,9],[12,10],
        [11,11],[10,12],[10,13],[11,14],[12,15],[12,16],[11,17],[10,18],[10,19],[11,20]
        ,[12,21],[12,22],[11,23],[10,24],[10,25],[11,26],[12,27],[12,28],[11,29],[10,30],[10,31]]
wave2 = [[10,0],[10,1],[11,2],[12,3],[12,4],[11,5],[10,6],[10,7],[11,8],[12,9],[12,10],
        [11,11],[10,12],[10,13],[11,14],[12,15],[12,16],[11,17],[10,18],[10,19],[11,20]
        ,[12,21],[12,22],[11,23],[10,24],[10,25],[11,26],[12,27],[12,28],[11,29],[10,30],[10,31]]





i = 0
while shipAnimationLast[-1][1] >= -20:
    matrixDisplay.Clear()
    frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
    for cell in battleshipTitle:
        frameCanvas.SetPixel(cell[0],cell[1],200,0,0)
    for cell in battleshipTitle:
        frameCanvas.SetPixel(cell[0] + 41,cell[1],200,0,0)
    for cell in battleshipTitle:
        frameCanvas.SetPixel(cell[0] + 82,cell[1],200,0,0)
    for cell in wave1:
        frameCanvas.SetPixel(cell[1],cell[0],4,55,242)
    for cell in wave2:
            frameCanvas.SetPixel(cell[1] - 2,cell[0] + 2,4,55,242)
    for cell in shipAnimation:
        frameCanvas.SetPixel(cell[1] + 5,cell[0] + 2,173,216,230)
    for cell in shipAnimation:
        frameCanvas.SetPixel(cell[1] + 20,cell[0] + 2,173,216,230)
    for cell in shipAnimation:
        frameCanvas.SetPixel(cell[1] + 35,cell[0] + 2,173,216,230)
    for cell in shipAnimationLast:
        frameCanvas.SetPixel(cell[1] + 50,cell[0] + 2,173,216,230)
    frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
    time.sleep(0.25)
    for cell in battleshipTitle:
        cell[0] -= 1
    for cell in shipAnimation:
        cell[1] -= 1
    for cell in shipAnimationLast:
        cell[1] -= 1
    if i % 2 == 0:
        for cell in wave1:
            cell[0] += 1
        for cell in wave2:
            cell[0] += 1
    else:
        for cell in wave1:
            cell[0] -= 1
        for cell in wave2:
            cell[0] -= 1
    i += 1

matrixDisplay.Clear()
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
    if placementProcess == 'manually':
        print("\n"*50)

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

debug = input("y/n")
if debug == "y":     
    mode = input("Single or Multiplayer mode? (s/m): ").lower()
    while mode != 's' and mode != 'm':
        mode = input("Please select 's' or 'm': ").lower()


    # Asks if player wants to place ships manually or automatically
    shipPlacementProcessBoolean1 = True
    while shipPlacementProcessBoolean1:
        player1ShipPlacementProcess = input("Player 1: Would you like to place the ships manually or randomly: ").lower().strip()
        if player1ShipPlacementProcess == "manually" or player1ShipPlacementProcess == "randomly":
            shipPlacementProcessBoolean1 = False
        else:
            print("Please enter \"manually\" or \"randomly\"")

    if mode == 's':
        player2ShipPlacementProcess = 'randomly'
    else:
        shipPlacementProcessBoolean2 = True
        while shipPlacementProcessBoolean2:
            player2ShipPlacementProcess = input("Player 2: Would you like to place the ships manually or randomly: ").lower().strip()
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
    if player1ShipPlacementProcess == 'manually':
        print("Player 1:")
    ship_placement(player1Board, player1ShipPlacementProcess, player1Ships)
    if player2ShipPlacementProcess == 'manually':
        print("Player 2:")
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

else:
    mode = "s"
    winner = "player"
    shipAnimation = [[7,31],[8,31],[6,32],[7,32],[8,32],[9,32],[6,33],[7,33],[8,33],
                    [9,33],[10,33],[6,34],[7,34],[8,34],[9,34],[10,34],[5,35],
                    [6,35],[7,35],[8,35],[9,35],[10,35],[5,36],[7,36],[8,36],[9,36],
                    [10,36],[5,37],[6,37],[7,37],[8,37],[9,37],[10,37],[5,38],[6,38],
                    [7,38],[8,38],[9,38],[10,38],[7,39],[8,39],[9,39],[10,39],[7,40],
                    [8,40],[9,40],[7,41],[8,41]]
    losingShipAnimation = [[0,9],[0,10],[1,9],[1,10],[1,11],[2,9],[2,10], [2,11],[2,12],[3,7],[3,8],[3,9],[3,10],[3,11],
                        [3,12],[4,7],[4,9],[4,10],[4,11],[4,12],[5,7],[5,8],[5,9],[5,10],[5,11],[5,12],[6,7],[6,8],[6,9],
                        [6,10],[6,11],[6,12],[7,8],[7,9],[7,10],[7,11],[7,12],[8,8],[8,9],[8,10],[8,11],[8,12],[9,8],[9,9],
                        [9,10],[9,11],[10,9],[10,10]]
    wave1 = [[10,0],[10,1],[11,2],[12,3],[12,4],[11,5],[10,6],[10,7],[11,8],[12,9],[12,10],
            [11,11],[10,12],[10,13],[11,14],[12,15],[12,16],[11,17],[10,18],[10,19],[11,20]
            ,[12,21],[12,22],[11,23],[10,24],[10,25],[11,26],[12,27],[12,28],[11,29],[10,30],[10,31]]
    wave2 = [[10,0],[10,1],[11,2],[12,3],[12,4],[11,5],[10,6],[10,7],[11,8],[12,9],[12,10],
            [11,11],[10,12],[10,13],[11,14],[12,15],[12,16],[11,17],[10,18],[10,19],[11,20]
            ,[12,21],[12,22],[11,23],[10,24],[10,25],[11,26],[12,27],[12,28],[11,29],[10,30],[10,31]]
    bomb = [[21,9],[20,9],[22,9],[21,8],[21,10]]
    player_text = [[3,2],[3,3],[3,4],[3,5],[3,6],[4,2],[4,4],[5,3],[7,2],[7,3],[7,4],[7,5],[7,6],[8,6],
                [9,6],[11,3],[11,4],[11,5],[11,6],[12,2],[12,5],[13,3],[13,4],[13,5],[13,6],[15,2],
                [16,3],[16,4],[16,5],[16,6],[17,2],[19,2],[19,3],[19,4],[19,5],[19,6],[20,2],[20,4],
                [20,6],[21,2],[21,4],[21,6],[23,2],[23,3],[23,4],[23,5],[23,6],[24,2],[24,4],[25,3],
                [25,5],[25,6]]
    computer_text = [[0,2],[0,3],[0,4],[0,5],[0,6],[1,2],[1,6],[2,2],[2,6],[4,2],[4,3],[4,4],[4,5],[4,6],
                    [5,2],[5,6],[6,2],[6,3],[6,4],[6,5],[6,6],[8,3],[8,4],[8,5],[8,6],[9,2],[10,3],[10,4],
                    [11,2],[12,3],[12,4],[12,5],[12,6],[14,2],[14,3],[14,4],[14,5],[14,6],[15,2],[15,4],
                    [16,3],[18,2],[18,3],[18,4],[18,5],[18,6],[19,6],[20,2],[20,3],[20,4],[20,5],[20,6],
                    [22,2],[23,2],[23,3],[23,4],[23,5],[23,6],[24,2],[26,2],[26,3],[26,4],[26,5],[26,6],
                    [27,2],[27,4],[27,6],[29,2],[29,3],[29,4],[29,5],[29,6],[30,2],[30,4],[31,3],[31,5],
                    [31,6]]
    win_text = [[7,7],[7,8],[7,9],[7,10],[8,11],[9,10],[10,11],[11,7],[11,8],[11,9],[11,10],[13,7],
                [13,8],[13,9],[13,10],[13,11],[15,7],[15,8],[15,9],[15,10],[15,11],[16,8],[17,9],[18,7],
                [18,8],[18,9],[18,10],[18,11],[20,7],[20,8],[20,9],[20,11],[21,7],[21,9],[21,11],[22,7],
                [22,9],[22,10],[22,11],[24,7],[24,8],[24,9],[24,11]]
    numb_1 = [[27,3],[27,6],[28,2],[28,3],[28,4],[28,5],[28,6],[29,6]]
    numb_2 = [[27,3],[27,6],[28,2],[28,5],[28,6],[29,3],[29,4],[29,6]]

    grid = []
    for row in range(screenHeight):
        for col in range(screenWidth):
            grid.append([col+34,row])     

    if mode == "s":
        if winner == "player":
            winner_num = None
        else:
            player_text = computer_text
            winner_num = None
    elif mode == "m":
        if winner == "Player 1":
            winner_num = numb_1
        else:
            winner_num = numb_2
                
    i = 0
    check = 0

    while True:
        matrixDisplay.Clear()
        frameCanvas = matrixDisplay.SwapOnVSync(frameCanvas)
        for cell in wave1:
            frameCanvas.SetPixel(cell[1],cell[0],4,55,242)
        for cell in wave2:
                frameCanvas.SetPixel(cell[1] - 2,cell[0] + 2,4,55,150)
        for cell in shipAnimation:
            frameCanvas.SetPixel(cell[1] + 5,cell[0] + 2,173,216,230)
        for cell in losingShipAnimation:
            if check >= 36:
                if losingShipAnimation.index(cell) <= 31:
                    frameCanvas.SetPixel(cell[0] - 15,cell[1],173,216,230)
            else:
                frameCanvas.SetPixel(cell[0] - 15,cell[1],173,216,230)
        time.sleep(.2)
        if check <= 14:
            for cell in shipAnimation:
                cell[1] -= 1
                if shipAnimation[0][1] == 16:
                    shipAnimation[0][1] -= 1
            for cell in losingShipAnimation:
                cell[0] += 1

        if check >= 18:
            if check == 18:
                shipAnimation[0][1] += 1
            if check <= 21:

                frameCanvas.SetPixel(bomb[0][0],bomb[0][1],200,20,20)
                for cell in bomb:
                    cell[0] -= 1
                    cell[1] -= 1
            elif check < 27:
                cell_num = 0
                for cell in bomb:
                    cell[0] -= 1
                    if cell_num != 0:
                        frameCanvas.SetPixel(cell[0], cell[1], 255, 165, 0)
                    frameCanvas.SetPixel(bomb[0][0],bomb[0][1],200,20,20)
                    cell_num += 1
            elif check <= 31:
                cell_num = 0
                for cell in bomb:
                    cell[0] -= 1
                    cell[1] += 1
                    if cell_num != 0:
                        frameCanvas.SetPixel(cell[0], cell[1], 255, 165, 0)
                    frameCanvas.SetPixel(bomb[0][0],bomb[0][1],200,20,20)
                    cell_num += 1
            elif check == 32:
                bomb.append([5,10])
                bomb.append([9,10])
                bomb.append([7,12])
                bomb.append([7,8])
                bomb.append([8,9])
                bomb.append([6,9])
                bomb.append([6,11])
                bomb.append([8,11])
                cell_num = 0
                frameCanvas.SetPixel(bomb[0][0],bomb[0][1],200,20,20)
                for cell in bomb:
                    print("bomb")
                    if cell_num != 0:
                        frameCanvas.SetPixel(cell[0], cell[1], 255, 165, 0)  
                    cell_num += 1
            elif check <= 35:
                cell_num = 0
                frameCanvas.SetPixel(bomb[0][0],bomb[0][1],200,20,20)
                for cell in bomb:
                    if cell_num != 0 and cell_num <= 8:
                        print("bomb")
                        frameCanvas.SetPixel(cell[0], cell[1], 255, 165, 0)   
                    if check > 33:
                        if cell_num > 8:
                            frameCanvas.SetPixel(cell[0], cell[1], 255, 117, 24)
                    cell_num += 1  
            elif 48 >= check >= 37:
                for cell in losingShipAnimation:
                    cell[1] += 1
            elif 84 > check > 48:
                for cell in shipAnimation:
                    cell[1] -= 1
                for cell in grid:
                    print("grid")
                    frameCanvas.SetPixel(cell[0], cell[1], 50, 50, 50)
                    cell[0] -= 1
                for cell in player_text:
                    print("player text")
                    frameCanvas.SetPixel(cell[0]+34, cell[1], 230, 0, 230)
                    cell[0] -= 1
                if winner_num != None:
                    for cell in winner_num:
                        print("winner num")
                        frameCanvas.SetPixel(cell[0]+34, cell[1], 255, 0, 255)
                        cell[0] -= 1
                for cell in win_text:
                    print("win text")
                    frameCanvas.SetPixel(cell[0]+34, cell[1] + 2, 255, 0, 255)
                    cell[0] -= 1
            elif check >= 84:
                time.sleep(5)
                break
        check += 1
        if i % 2 == 0:
            for cell in wave1:
                cell[0] += 1
            for cell in wave2:
                cell[0] += 1
        else:
            for cell in wave1:
                cell[0] -= 1
            for cell in wave2:
                cell[0] -= 1
        i += 1
        
        
                
    print("\nExiting cleanly...")
    matrixDisplay.Clear()