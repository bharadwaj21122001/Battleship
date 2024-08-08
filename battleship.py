"""
Battleship Project
Name: M.Bharadwaj
Roll No: 2023501046
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):                                           # declared a dictionary namely datain this function we declared variable names in to the dictionary
    data["row"] = 10                                                     # declared how many rows should the grid has
    data["col"] = 10                                                     # declared how many columns should the grid has                                                   
    data["Boardsize"] = 500                                              # declared the size of game board
    data["CellSize"] = data["Boardsize"] // data["row"]                  # declared the size of each cell in board
    data["ComputerBoard"] = emptyGrid(data["row"],data["col"])           # build the computer board
    data["UserBoard"] = emptyGrid(data["row"],data["col"])               # build the user board
    data["User_ship"] = 0                                                # declared how many ships does user has
    data["Computer_ship"] = 0                                         # declared how many ships does computer 
    data["computer"]=addShips(data["ComputerBoard"], data["Computer_ship"]) # declared the player as computer
    data["user"]=addShips(data["UserBoard"], data["User_ship"])          # declared the player as user
    # data["Temporary_ship"] = test.testShip()
    data["Temporary_ship"] = []                                          # considered a temporary ship to keep track on number of ships placed on board
    data["Winner"] = None                                                # declared the variable winner to check whether the game is won by user or computer  or its draw
    data["Max_turns"] = 50                                               # declared maximum number of turns that can be made
    data["current_turns"] = 0                                            # declared variable to keep track on number of turns made
    return None


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):                    #here in this function we will visualize the view of comp grid and user grid
    drawGrid(data,compCanvas,data["ComputerBoard"],showShips=False)                            # called draw grid function to draw computer board and hided the ships placed
    drawGrid(data,userCanvas,data["UserBoard"],showShips=True)                                 # called draw grid function to draw user board 
    drawShip(data,userCanvas,data["Temporary_ship"])                                           # drawing the ships which are placed on board
    drawGameOver(data,userCanvas)                                                              # checking the winner and displaying the message
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":                               # this function is used for key pressed events, keysym = key symbol
        makeModel(data)                                        # checks whether the pressed key in enter if its then restarts the game
    return None


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):                         # this function is for mouse pressed events
    if data["Winner"] == None:
        cell = getClickedCell(data,event)                    # called the function getclickedcell 
        if board == "user":                                  # checking the event done on user board and sending the clicked location to mark cell
            clickUserBoard(data,cell[0],cell[1])
        if board == "comp" and data["User_ship"] == 5:       # here we are swapping the turns of computer and user
            runGameTurn(data,cell[0],cell[1])
    return None

#### STAGE 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):                             # this function is draw the empty grid
    grid = []
    for i in range(rows):
        rows = []
        for j in range(cols):                          # all the elements in grid are set to EMPTY_UNCLICKED
            rows.append(EMPTY_UNCLICKED)
        grid.append(rows)
    return grid

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():                                    # this function is create ships
    row = random.randint(1,8)
    col = random.randint(1,8)
    veri_horiz = random.randint(0,1)
    if veri_horiz == 1:
        ship=[[row-1,col],[row,col],[row+1,col]]       # to create ship in horizontal or vertical
    else:
         ship=[[row,col-1],[row,col],[row,col+1]]

    return ship


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):                            # this function is to check the coordinates are not clicked repetadly
    for i,j in ship:
        if grid[i][j] != EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):                    # this function is to check the ship to be placed
    count = 0
    while count < numShips:
        ship = createShip()                      # called createShip() function to create ship
        if checkShip(grid,ship):
            count += 1                           # keeping the track on how many ships are created
            for row in ship:
                grid[row[0]][row[1]] = SHIP_UNCLICKED
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):                # this function is to draw grid on boards
    CellSize = data["CellSize"]
    for row in range(data["row"]):
        for col in range(data["col"]):
            x1 = col * CellSize
            y1 = row * CellSize
            x2 = x1 + CellSize
            y2 = y1 + CellSize
            
            if grid[row][col] == EMPTY_UNCLICKED:
                color = "blue"
            elif grid[row][col] == SHIP_UNCLICKED and showShips == True:
                color = "yellow"
            elif grid[row][col] == SHIP_UNCLICKED and showShips == False:           # blue color is to hid the ships
                color = "blue"
            elif grid[row][col] == SHIP_CLICKED:
                color = "red"
            elif grid[row][col] == EMPTY_CLICKED:
                color = "white"
            
            canvas.create_rectangle(x1,y1,x2,y2, fill = color)          # creating the canvas using tkinter
    canvas.pack()
    return 


### STAGE 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):                                                   # checking whether the clicked cell are in vertical or not
    ship.sort()
    if ship[0][1] == ship[1][1] == ship[2][1]:
        if abs(ship[0][0] - ship[1][0]) == abs(ship[1][0] - ship[2][0]) == 1:
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):                                                 # checking whether the clicked cell are in horizontal or not
    ship.sort()
    if ship[0][0] == ship[1][0] == ship[2][0]:
        if abs(ship[0][1] - ship[1][1]) == abs(ship[1][1] - ship[2][1]) == 1:
            return True
    return False

'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):                                        # getting the location of cell and mouse click location
    col = int(event.x) // data["CellSize"]
    row = int(event.y) // data["CellSize"]
    return [int(row),int(col)]
    # row = data["row"]
    # col = data["col"]
    # CellSize = data["CellSize"]
    # x = event.x
    # y = event.y
    # for i in range(row):
    #     for j in range(col):
    #         x1 = j * CellSize
    #         y1 = i * CellSize
    #         x2 = x1 + CellSize
    #         y2 = y1 + CellSize
    #         if x1 < x < x2 and y1 < y < y2:
                # return [i,j]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    CellSize = data["CellSize"]
    for i,j in ship:                                          # this function is draw ship on board using canvas and tkinter
        x1 = j * CellSize
        y1 = i * CellSize
        x2 = x1 + CellSize
        y2 = y1 + CellSize
        canvas.create_rectangle(x1,y1,x2,y2, fill = "white")
    return None


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) != 3:
        return False                                      # checking whether the ship is valid or not
    for row,col in ship:
        if grid[row][col] == SHIP_CLICKED:
            return False
    if checkShip(grid,ship) == False or isVertical(ship) == False and isHorizontal(ship) == False:
        return False

    return True 

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if data["User_ship"] == 5:
        return                                               # this function is place ship on boards
    else:
        User_board = data["UserBoard"]
        
        if shipIsValid(User_board,data["Temporary_ship"]):
            for i,j in data["Temporary_ship"]:
                User_board[i][j] = SHIP_UNCLICKED
            data["User_ship"] += 1                         # incrementing the count of user ships
            data["Temporary_ship"].clear()
        else:
            print("Invalid")
        data["Temporary_ship"].clear()

        if shipIsValid(data["ComputerBoard"],data["Temporary_ship"]):
            for row,col in data["Temporary_ship"]:
                data["ComputerBoard"][row][col] = SHIP_UNCLICKED
                data["Computer_ship"] += 1
                data["Temporary_ship"].clear()
        else:
            print("Invalid")
        data["Temporary_ship"].clear()
    
    if data["User_ship"] == 5:
        print("You can start game!!")

    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if [row,col] in data["Temporary_ship"]:
        return 
    data["Temporary_ship"].append([row,col])                  # appending the coordinates of clicked cell into temporary ship variable

    if len(data["Temporary_ship"]) == 3:
        placeShip(data)
    return 


### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):                      # this function is update board after every mouse click event
    if board[int(row)][int(col)] == SHIP_UNCLICKED:
        board[int(row)][int(col)] = SHIP_CLICKED
        if isGameOver(board):
            data["Winner"] = player                                  # checking whether every ship in board is clicked or not
    elif board[int(row)][int(col)] == EMPTY_UNCLICKED:
        board[int(row)][int(col)] = EMPTY_CLICKED
        
    return None


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):                                 # this function will handle computer and user click events
    if data["ComputerBoard"][row][col] == SHIP_CLICKED or data["ComputerBoard"][row][col] == EMPTY_CLICKED:
        return None
    else:
        updateBoard(data,data["ComputerBoard"],int(row),int(col),"user")
    
    cell = getComputerGuess(data["user"])                        # this is for computer's turn
    updateBoard(data,data["UserBoard"],cell[0],cell[1],"comp")
    data["current_turns"] += 1                                   # increments to check whether the turns are completed or not
    if data["current_turns"] > data["Max_turns"]:
        data["Winner"] = "draw"                                  # declaring the game is draw if current turns are equal are more than maximum turns
    return 


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):                                     # this function is to computers turns
    while True:
        row = random.randint(1,8)                                # excluding the firt and last row
        col = random.randint(1,8)                                # excluding the first and last column
        if board[row][col] == SHIP_CLICKED or board[row][col] == EMPTY_CLICKED:  # checking whether the clicked cell is on user board
            continue
        else:
            return [row,col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(10):
        for col in range(10):                                  # checking whether all the ships are clicked or not
            if board[row][col] == SHIP_UNCLICKED:
                return False

    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["Winner"] == "user":                                   # if the winner is user then printing congratulation and giving the chance to continue game
        canvas.delete("all")
        canvas.create_text(200,30,text = "Congratulation! Yoou have won the game", fill = "black")
        canvas.create_text(200,50,text = "Press Enter key to restart game again!", fill = "black")

    elif data["Winner"] == "comp":
        canvas.delete("all")
        canvas.create_text(200,30,text = "You have lost game!", fill = "black")          # if the winner is computer printing lost game and giving the change to continuing the game
        canvas.create_text(200,50,text = "Press Enter key to restart game again!", fill = "black")
    
    elif data["Winner"] == "draw":
        canvas.delete("all")
        canvas.create_text(200,30, text = "You are out of moves!" , fill = "black")       # if its draw then printing its draw and giving chance to continue the game
        canvas.create_text(200,50, text = "Press Enter key to restart the game", fill = "black")
    canvas.pack()
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    # test.stage1Tests()
    # test.testEmptyGrid()
    # test.testCreateShip()
    # test.testCheckShip()
    # test.testAddShips()
    # test.testDrawGrid()

    ## Uncomment these for STAGE 2 ##
    
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    # test.stage2Tests()
    # test.testIsVertical()
    # test.testIsHorizontal()
    # test.testGetClickedCell()
    # test.testDrawShip()
    # test.testShipIsValid()

    

    ## Uncomment these for STAGE 3 ##
    
    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    # test.stage3Tests()
    # test.testUpdateBoard()
    # test.testGetComputerGuess()
    # test.testIsGameOver()

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
 