# modules
import pygame
import tkinter as tk
from PIL import ImageTk, Image
import random
import time
import sys

# Screen settings
MAX_DISPLAY_WIDTH = 1000
MAX_DISPLAY_HEIGHT = 700
MAX_BLOCK_SIZE = 150
HEADER_HEIGHT = 30
SYSTEM_FONT = "couriernew"
TKINTER_FONT = "Courier"

# Images
IMG_UNTOUCHED_SQUARE = pygame.image.load("img/square_untouched.png")
IMG_FLAG = pygame.image.load("img/square_flagged.png")
IMG_BLANK_SQUARE = pygame.image.load("img/square_blank.png")
IMG_MINE = pygame.image.load("img/square_mine.png")
IMG_SQUARE_1 = pygame.image.load("img/square_1.png")
IMG_SQUARE_2 = pygame.image.load("img/square_2.png")
IMG_SQUARE_3 = pygame.image.load("img/square_3.png")
IMG_SQUARE_4 = pygame.image.load("img/square_4.png")
IMG_SQUARE_5 = pygame.image.load("img/square_5.png")
IMG_SQUARE_6 = pygame.image.load("img/square_6.png")
IMG_SQUARE_7 = pygame.image.load("img/square_7.png")
IMG_SQUARE_8 = pygame.image.load("img/square_8.png")
# Images for black squares
IMG_BLANK_SQUARE_BLACK = pygame.image.load("img/square_blank_black.png")
IMG_MINE_BLACK = pygame.image.load("img/square_mine_black.png")
IMG_SQUARE_BLACK_1 = pygame.image.load("img/square_1_black.png")
IMG_SQUARE_BLACK_2 = pygame.image.load("img/square_2_black.png")
IMG_SQUARE_BLACK_3 = pygame.image.load("img/square_3_black.png")
IMG_SQUARE_BLACK_4 = pygame.image.load("img/square_4_black.png")
IMG_SQUARE_BLACK_5 = pygame.image.load("img/square_5_black.png")
IMG_SQUARE_BLACK_6 = pygame.image.load("img/square_6_black.png")
IMG_SQUARE_BLACK_7 = pygame.image.load("img/square_7_black.png")
IMG_SQUARE_BLACK_8 = pygame.image.load("img/square_8_black.png")

# Image Arrays (indices matter to the code)
IMG_SQUARES = [IMG_BLANK_SQUARE, IMG_SQUARE_1, IMG_SQUARE_2, IMG_SQUARE_3, IMG_SQUARE_4, IMG_SQUARE_5, IMG_SQUARE_6, IMG_SQUARE_7, IMG_SQUARE_8, IMG_MINE]
IMG_SQUARES_BLACK = [IMG_BLANK_SQUARE_BLACK, IMG_SQUARE_BLACK_1, IMG_SQUARE_BLACK_2, IMG_SQUARE_BLACK_3, IMG_SQUARE_BLACK_4, IMG_SQUARE_BLACK_5, IMG_SQUARE_BLACK_6, IMG_SQUARE_BLACK_7, IMG_SQUARE_BLACK_8, IMG_MINE_BLACK]

# Tkinter Icon
TKINTER_ICON_PATH = "img/white.ico"
# End Screen Images
SMILEY_WIN = "img/smiley_win.png"
SMILEY_LOSE = "img/smiley_lose.png"


# ================================================================
# CLASSES
# ================================================================

class Colour:
  def __init__(self):
    self.minesweeper_gray = (175, 175, 175)
    self.background_colour = (100, 100, 100)
    self.darker_gray = (75, 75, 75)
    self.dark_gray = (100, 100, 100)
    self.gray = (150, 150, 150)
    self.light_gray = (215, 215, 215)
    self.white = (255, 255, 255)
    self.black = (0, 0, 0)
    self.red = (255, 0, 0)

# Mouse controller class
class Mouse:
  def __init__(self):
    self.leftDown = False
    self.rightDown = False

# A helper class for timing the duration of a game
class Timer:
  def __init__(self):
    self.start = 0
    self.end = 0

  def startTimer(self):
    self.start = time.perf_counter()

  def getTime(self):
    self.end = time.perf_counter()
    timer = int(self.end - self.start) + 1
    if timer > 999:
      timer = 999
    return timer
# A stop timer function is pointless in this program.

# Menu logic (uses Tkinter library)
class Menu(tk.Frame):
  def __init__(self, parent):
    # Init
    tk.Frame.__init__(self, parent)
    self.parent = parent
    # Set icon
    self.parent.iconbitmap(TKINTER_ICON_PATH)
    # Set window name
    self.parent.winfo_toplevel().title("Welcome")
    # Create input validation object
    vcmd = (self.register(self.onValidate), "%S")
    # Keep window size
    self.parent.resizable(False, False)

    # Widget creation
    # Labels
    title = tk.Label(self, text = "Welcome to Minesweeper")
    prompt1 = tk.Label(self, text = "Width")
    prompt2 = tk.Label(self, text = "Height")
    prompt3 = tk.Label(self, text = "# Mines")
    optionlabel = tk.Label(self, text = "OR choose a difficulty:")
    spacer = tk.Label(self, text = "") # Something to separate the custom game from the difficulty buttons
    # Entry boxes
    self.widthbox = tk.Entry(self, width = 3, validate = "key", validatecommand = vcmd)
    self.heightbox = tk.Entry(self, width = 3, validate = "key", validatecommand = vcmd)
    self.minebox = tk.Entry(self, width = 3, validate = "key", validatecommand = vcmd)
    # Buttons
    play = tk.Button(self, text = "Play", command = self.playCustom)
    easy = tk.Button(self, text = "Easy", command = self.playEasy)
    medium = tk.Button(self, text = "Medium", command = self.playMedium)
    hard = tk.Button(self, text = "Hard", command = self.playHard)
    quit = tk.Button(self, text = "Quit Game", command = self.quit)

    # Config
    # Title
    title.config(font=(TKINTER_FONT, 22))
    # Custom Game Input
    prompt1.config(font=(TKINTER_FONT, 16))
    prompt2.config(font=(TKINTER_FONT, 16))
    prompt3.config(font=(TKINTER_FONT, 16))
    self.widthbox.config(font=(TKINTER_FONT, 16))
    self.heightbox.config(font=(TKINTER_FONT, 16))
    self.minebox.config(font=(TKINTER_FONT, 16))
    play.config(width = 10, font = (TKINTER_FONT, 12))
    # Choose difficulty
    optionlabel.config(font=(TKINTER_FONT, 16))
    easy.config(width = 10, font = (TKINTER_FONT, 12))
    medium.config(width = 10, font = (TKINTER_FONT, 12))
    hard.config(width = 10, font = (TKINTER_FONT, 12))
    # Quit game
    quit.config(width = 10, font = (TKINTER_FONT, 12))

    # Packing
    # Title
    title.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5)
    # Custom Game Input
    prompt1.grid(row = 1, column = 1, sticky = "E")
    self.widthbox.grid(row = 1, column = 2, sticky = "W")
    prompt2.grid(row = 2, column = 1, sticky = "E")
    self.heightbox.grid(row = 2, column = 2, sticky = "W")
    prompt3.grid(row = 3, column = 1, sticky = "E")
    self.minebox.grid(row = 3, column = 2, sticky = "W")
    play.grid(row = 4, column = 1, columnspan = 2, padx = 3, pady = 3)
    # Spacer
    spacer.grid(row = 5, column = 0, columnspan = 2)
    # Choose difficulty
    optionlabel.grid(row = 6, column = 0, columnspan = 4)
    easy.grid(row = 7, column = 0, padx = 3, pady = 3, sticky = "N")
    medium.grid(row = 7, column = 1, columnspan = 2, padx = 3, pady = 3, sticky = "N")
    hard.grid(row = 7, column = 3, padx = 3, pady = 3, sticky = "N")
    # Quit game
    quit.grid(row = 8, column = 1, columnspan = 2, padx = 3, pady = 3)

  # Validate input function
  def onValidate(self, char):
    try:
      float(char)
      return True
    except ValueError:
      return False

  def playCustom(self):
    try:
      width = int(self.widthbox.get())
      height = int(self.heightbox.get())
      mines = int(self.minebox.get())
    except ValueError:
      return

    # We cap the size of a board at 50 X 50, and we make sure the size of the board is at least 1 X 1
    # It's easier to do it here than in the dialog box
    if width > 50:
      width = 50
    elif width <= 0:
      width = 1
    if height > 50:
      height = 50
    elif height <= 0:
      height = 1
    # We make sure there are always less mines than there are squares
    if mines >= (width * height):
      mines = ((width * height) - 1)

    self.parent.destroy()
    startGame(width, height, mines)

  def playEasy(self):
    self.parent.destroy()
    startGame(9, 9, 10)

  def playMedium(self):
    self.parent.destroy()
    startGame(18, 14, 40)

  def playHard(self):
    self.parent.destroy()
    startGame(24, 20, 99)

  def quit(self):
    self.parent.destroy()
    return

class EndScreen(tk.Frame):
  def __init__(self, parent, isWin, owidth, oheight, obombs):
    # Init
    tk.Frame.__init__(self, parent)
    self.parent = parent
    # Set icon
    self.parent.iconbitmap(TKINTER_ICON_PATH)
    # Set window name
    self.parent.winfo_toplevel().title("Play again?")
    # Keep window size
    self.parent.resizable(False, False)
    # Remember the last board's dimensions
    self.owidth = owidth
    self.oheight = oheight
    self.obombs = obombs
    # Determine window message
    if isWin:
      message = "Congrats, you won!"
    else:
      message = "Oops, you hit a mine!"

    # Widget creation
    # Labels
    if isWin:
      img = ImageTk.PhotoImage(Image.open(SMILEY_WIN))
    else:
      img = ImageTk.PhotoImage(Image.open(SMILEY_LOSE))
    title = tk.Label(self, text = message)
    image = tk.Label(self, image = img)
    image.image = img
    # Buttons
    btnMenu = tk.Button(self, text = "Menu", command = self.toMenu)
    btnTryAgain = tk.Button(self, text = "Play Again", command = self.tryAgain)
    btnQuit = tk.Button(self, text = "Quit", command = self.quit)

    # Config
    title.config(font=(TKINTER_FONT, 22))
    btnMenu.config(width = 10, font = (TKINTER_FONT, 12))
    btnTryAgain.config(width = 10, font = (TKINTER_FONT, 12))
    btnQuit.config(width = 10, font = (TKINTER_FONT, 12))

    # Packing
    title.grid(row = 0, column = 0, columnspan = 3, padx = 3, pady = 3)
    image.grid(row = 1, column = 0, columnspan = 3)
    btnMenu.grid(row = 2, column = 0, padx = 10, pady = 10)
    btnTryAgain.grid(row = 2, column = 1, padx = 10, pady = 10)
    btnQuit.grid(row = 2, column = 2, padx = 10, pady = 10)

  def toMenu(self):
    self.parent.destroy()
    root = tk.Tk()
    Menu(root).pack()
    root.mainloop()

  def tryAgain(self):
    self.parent.destroy()
    startGame(self.owidth, self.oheight, self.obombs)

  def quit(self):
    self.parent.destroy()

# A class to define a single square of the Minesweeper board
class Square:
  def __init__(self, value, x, y, size):
    self.active = False
    self.flagged = False
    self.black = False
    self.value = value
    self.x = x
    self.y = y
    self.rect = pygame.Rect(size*x, size*y + HEADER_HEIGHT, size, size)
    self.image = pygame.transform.scale(IMG_UNTOUCHED_SQUARE, (size, size))
    self.size = size


# ================================================================
# HELPER FUNCTIONS
# ================================================================

# Returns an array of the squares adjacent to the given coordinates
def getAdjacentSquares(board, x, y):
  squares = []
  height = len(board)
  width = len(board[0])
  for i in range(y-1, y+2):
    for j in range(x-1, x+2):
      # bounds checking
      if j >= 0 and i >= 0 and j < width and i < height:
        squares.append(board[i][j])
  return squares

# Sets boolean flags in the board for whether they are black or white squares (for visual reasons)
def checkerBoard(board):
  r = 0
  c = 0
  for y in board:
    c = 0
    for x in y:
      s = r + c
      if s % 2 == 0:
        x.black = True
      else:
        x.black = False
      c = c + 1
    r = r + 1

  

# ================================================================
# BOARD INITIALIZATION FUNCTIONS
# ================================================================

# This is a function used for generating the mine field
# Inputs are field size (x and y values), number of bombs (int), and where the user clicked (Coord)
# The bombs will never appear within two squares of the cursor position.
# The grid must have an X of at least 4 and a Y of at least 4 (but that's handled elsewhere)
# A 2d array is returned, populated by mines and empty squares.
def generateField(width, height, numBombs, click):
  # Generate an empty grid to populate
  grid = []
  for y in range(height):
    row = []
    for x in range(width):
      row.append(0)
    grid.append(row)

  # This returns an empty field if the user hasn't clicked yet
  if not click:
    return grid

  # We need to figure out which squares aren't allowed to have bombs in them.
  # The square you click in can never have a bomb in it
  # The squares adjacent to that square never have bombs in them, UNLESS THERE ARE TOO MANY BOMBS TO ACCOMOMDATE
  invalidSquares = []
  for y in range(click[1] - 1, click[1] + 2):
    for x in range(click[0] - 1, click[0] + 2):
      if x >= 0 and y >= 0 and x < width and y < height:
        invalidSquare = []
        invalidSquare.append(x)
        invalidSquare.append(y)
        invalidSquares.append(invalidSquare)
        # Here we remove the center square from the list of invalid squares. We add it in manually once we finish bomb accommodation
        if x == click[0] and y == click[1]:
          invalidSquares.pop()

  # Here we check the bomb count vs the size of the board, and if we have to fill some invalid squares we make some of them valid
  # Let's say we have a 10 X 10 grid with 94 bombs in it.
  validSquareCount = (width * height) - numBombs  # That means validSquareCount will be equal to 6
  # The count of a will vary (if the user clicks on an edge or corner)
  # But let's say the user clicked on a center square, which means there are 8 items in invalidSquares (we add 1 for the square we clicked on)
  a = validSquareCount - (len(invalidSquares) + 1)
  # In our example, a will be equal to -3
  # Because a is negative, we'll take off 3 out of the 8 squares in invalidSquares
  if a < 0:
    random.shuffle(invalidSquares) # We'll do so randomly
    for i in range(a, 0):
      invalidSquares.pop(0)
  # Here we make sure that the square we clicked on is in the list of invalidSquares
  clickSquare = []
  clickSquare.append(click[0])
  clickSquare.append(click[1])
  invalidSquares.append(clickSquare)

  # We need to calculate the probability of a bomb being in any given square.
  try:
    prob = numBombs/((width * height) - len(invalidSquares))
  except ZeroDivisionError:
    prob = 1
  
  bombs = 0
  # We plant bombs until there are no more bombs to plant
  while bombs < numBombs:
    for y in range(len(grid)):
      for x in range(len(grid[y])):
        c = []
        c.append(x)
        c.append(y)
        # We check that where we're planting is not near the cursor and that we didn't already plant there
        if c not in invalidSquares and grid[y][x] != 9:
          isBomb = random.random() < prob
          if isBomb:
            grid[y][x] = 9
            bombs = bombs + 1
        if bombs == numBombs:
          break
      if bombs == numBombs:
        break
    if bombs == numBombs:
      break
  
  # We should now have a grid full of bombs. Next we need to figure out for each square how many bombs are adjacent to it.
  # For each square
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      # If the square's not a bomb:
      if grid[y][x] == 0:
        c = 0
        # Check adjacent squares
        for i in range((y-1), (y+2)):
          for j in range((x-1), (x+2)):
            if j >= 0 and i >= 0 and j < width and i < height:
              if grid[i][j] == 9:
                c = c + 1
        grid[y][x] = c

  return grid


# This function joins the integer grid initialization and the drawing grid initialization.
# Basically this creates the grid of clickable objects.
def initBoard(field, size):
  # init
  board = []
  dheight = len(field)
  dwidth = len(field[0])
  
  # create objects
  for y in range(dheight):
    row = []
    for x in range(dwidth):
      square = Square(field[y][x], x, y, size)
      row.append(square)
    board.append(row)

  # Checker board
  checkerBoard(board)

  # Set images
  setStartImages(board)

  # return
  return board


def setStartImages(board):
  for y in board:
    for x in y:
      squareImageChange(x, IMG_UNTOUCHED_SQUARE)



# ================================================================
# BOARD DRAWING FUNCITONS
# ================================================================

def getScreenSize(bwidth, bheight):
  # We're going to return these 3 variables
  screenWidth = 0
  screenHeight = 0
  blockSize = 0

  # We basically check each size of block until we find a size that fits in the display
  c = MAX_BLOCK_SIZE
  while c > 0:
    potwidth = bwidth * c
    potheight = bheight * c
    if potwidth <= MAX_DISPLAY_WIDTH and potheight <= (MAX_DISPLAY_HEIGHT - HEADER_HEIGHT):
      screenWidth = potwidth
      screenHeight = potheight
      blockSize = c
      break
    c = c - 1

  return screenWidth, screenHeight, blockSize

def drawBoard(display, board, numBombsLeft, currTime):
  # Object declaration happens in the initBoard() function when we're making all the squares

  # Init
  colour = Colour()
  font = pygame.font.SysFont(SYSTEM_FONT, HEADER_HEIGHT)
  displayWidth = display.get_width()

  # Header paint
  header = pygame.Surface((displayWidth, HEADER_HEIGHT))
  header.fill(colour.minesweeper_gray)

  # Num mines surface logic
  flagIcon = pygame.transform.scale(IMG_FLAG, (HEADER_HEIGHT, HEADER_HEIGHT))
  flagNum = font.render(str(numBombsLeft), True, colour.black, colour.minesweeper_gray)

  # Timer surface logic
  timeObj = font.render(str(currTime), True, colour.black, colour.minesweeper_gray)
  timerSpace = int(displayWidth - (HEADER_HEIGHT * 2))

  # Painting
  # Header
  display.blit(header, (0, 0))
  # Print icons if the display is wide enough
  # Flag icon
  if displayWidth >= HEADER_HEIGHT:
    display.blit(flagIcon, (0,0))
  # Num Mines
  if displayWidth >= HEADER_HEIGHT * 4:
    display.blit(flagNum, (HEADER_HEIGHT, 0))
  # Timer
  if displayWidth >= HEADER_HEIGHT * 7:
    display.blit(timeObj, (timerSpace, 0))
  # Board
  for y in board:
    for x in y:
        display.blit(x.image, x.rect)

  # Update
  pygame.display.update()

# Sets the new image for a clicked square
def squareImageChange(square, image):
  square.image = pygame.transform.scale(image, (square.size, square.size))


# ================================================================
# CLICK FUNCTIONS
# ================================================================

# Highlights squares adjacent to the mouse if the user is holding left mouse and right mouse buttons
def mouseSweep(mouse, mousePos, board):
  if mouse.leftDown and mouse.rightDown:
    # We scan the board
    for y in board:
      for square in y:
        # When we find the square the mouse is on
        if square.rect.collidepoint(mousePos):
          # Get the adjacent squares
          adj = getAdjacentSquares(board, square.x, square.y)
    # Once we know what squares to paint blank, we loop the board again
    for y in board:
      for square in y:
        # We only want to affect untouched unflagged squares
        if not square.active and not square.flagged:
          if square in adj:
            if square.black:
              squareImageChange(square, IMG_BLANK_SQUARE_BLACK)
            else:
              squareImageChange(square, IMG_BLANK_SQUARE)
          else:
            squareImageChange(square, IMG_UNTOUCHED_SQUARE)

  # If we're not double clicking
  else:
    # For all blank non-flagged squares:
    for y in board:
      for square in y:
        if not square.active and not square.flagged:
          # We change the image (back) to a blank square
          squareImageChange(square, IMG_UNTOUCHED_SQUARE)
          

# Handles when the user does a double click (meaning right mouse and left mouse buttons are held down and then released)
def handleDoubleClick(board, clickPos):
  numDug = 0
  height = len(board)
  width = len(board[0])
  # We check for the square we clicked
  for y in board:
    for square in y:
      # Once we find it, we make sure it's already been checked
      if square.rect.collidepoint(clickPos) and square.active:
        val = square.value
        c = 0
        # Here we check for flagged squares around the square we're checking
        adj = getAdjacentSquares(board, square.x, square.y)
        for i in adj:
          if i.flagged:
            c = c + 1
        # If the number of flags around the square is equal to the value of the square
        if val == c:
          for i in adj:
            v = clickSquare(i)
            if v == 9:
              return "bomb"
            if v >= 0 and v < 9:
              numDug = numDug + 1
            # That click includes checking for a cascade
            if v == 0:
              numDug = numDug + cascade(board, i.x, i.y)
  return numDug
        
# A function that handles the first click on the board and returns the coordinates of the clicked square
def firstClick(board, clickPos):
  for y in board:
    for square in y:
      if square.rect.collidepoint(clickPos) and not square.flagged:
        return square.x, square.y

# Handles click logic in the game. Returns the number of squares affected by the click
def handleClick(board, clickPos):
  numDug = 0
  for y in board:
    for square in y:
      if square.rect.collidepoint(clickPos):
        val = clickSquare(square)
        if val == 9:
          return "bomb"
        if val >= 0 and val < 9:
          numDug = 1
        if val == 0:
          numDug = numDug + cascade(board, square.x, square.y)
        return numDug
  return numDug

# Helper function for clicking and double click functions
def clickSquare(square):
  if not square.active and not square.flagged:
    square.active = True
    if square.black:
      squareImageChange(square, IMG_SQUARES_BLACK[square.value])
    else:
      squareImageChange(square, IMG_SQUARES[square.value])
    return square.value
  return -1

# Function that handles when a square of value 0 is clicked
# Basically we click every surrounding square if we've found a blank one, since we can guarantee there are no bombs around it
# For back-story, this used to be a recursive function.
# The problem with that was there was sometimes a stack overflow because of the way it was recurring.
# The program kept going down the same tree instead of spreading out like it was supposed to.
# So, this idea of holding an array of spots to dig was born.
def cascade(board, x, y):
  numDug = 0
  height = len(board)
  width = len(board[0])

  # This variable keeps track of all the squares of value 0 that have been dug up by the program.
  # The first square was dug up in the click/double-click method, but we put it in the array here because it's the start point.
  squaresToDig = []
  squaresToDig.append(board[y][x])

  # We loop until all the squares needed to be dug up are
  while squaresToDig:
    x = squaresToDig[0].x
    y = squaresToDig[0].y
    adj = getAdjacentSquares(board, x, y)
    for i in adj:
      val = clickSquare(i)
      # We keep track of how many squares we dug up
      if val >= 0 and val < 9:
        numDug = numDug + 1
      # If we dug up a blank square, we add it to the end of the array so that we'll dig around it
      if val == 0:
        squaresToDig.append(i)
    # We get rid of the square we just did and get to the next in line
    squaresToDig.pop(0)

  return numDug

# Handles logic for right click (eg. flagging squares)
# The number returned helps the program keep track of how many flags are placed
def handleMark(board, clickPos):
  for y in board:
    for square in y:
      if square.rect.collidepoint(clickPos) and not square.active:
        if square.flagged:
          square.flagged = False
          squareImageChange(square, IMG_UNTOUCHED_SQUARE)
          return 1
        else:
          square.flagged = True
          squareImageChange(square, IMG_FLAG)
          return -1
  return 0

# Logic to handle different mouse states.
# If action is 1, it's a left click. If it's 3, it's a right click.
def getMouseActionDown(mouseState, action):
  if action == 1:
    mouseState.leftDown = True
    if mouseState.rightDown:
      return "double"
    else:
      return "click"
  elif action == 3:
    mouseState.rightDown = True
    if mouseState.leftDown:
      return "double"
    else:
      return "mark"
  return "nothing"
def getMouseActionUp(mouseState, action):
  if action == 1:
    mouseState.leftDown = False
  elif action == 3:
    mouseState.rightDown = False
  return "nothing"



# ================================================================
# GAME LOGIC
# ================================================================

def startGame(bwidth, bheight, numBombs):
  gameState = ""
  # This variable is how we determine if the board is clear
  numActive = ((bwidth * bheight) - numBombs)
  # This is for the display, to show how many "bombs" are flagged
  numBombsLeft = numBombs
  # This is for the timer
  timer = Timer()

  # Set board dimensions
  width, height, blockSize = getScreenSize(bwidth, bheight)
  height = height + HEADER_HEIGHT
  # We call this twice thanks to a pygame glitch...
  display = pygame.display.set_mode((width, height))
  display = pygame.display.set_mode((width, height))
  # Generate the initial field
  field = generateField(bwidth, bheight, numBombs, 0)
  # Create the squares to draw
  board = initBoard(field, blockSize)
  
  # Cursor logic initialization
  mouse = Mouse()
  click = 0

  # This is here so that in between games you can't click on the screen and mess things up for the next game
  for event in pygame.event.get():
    continue

  # This is logic to control the blank board (before the user clicks on a square)
  while 1:
    drawBoard(display, board, numBombsLeft, 0)
    for event in pygame.event.get():
      action = ""
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        action = getMouseActionDown(mouse, event.button)
      elif event.type == pygame.MOUSEBUTTONUP:
        action = getMouseActionUp(mouse, event.button)

      if action == "click":
        click = firstClick(board, pygame.mouse.get_pos())
      elif action == "mark":
        numBombsLeft = numBombsLeft + handleMark(board, pygame.mouse.get_pos())
    if click:
      break

  # Once we know where the user clicked, we can generate the board
  field = generateField(bwidth, bheight, numBombs, click)
  board = initBoard(field, blockSize)
  numBombsLeft = numBombs

  # Do the first click while counting how many squares were clicked
  numActive = numActive - handleClick(board, pygame.mouse.get_pos())
  timer.startTimer()

  # This logic controls the game board
  while 1:
    for event in pygame.event.get():
      action = ""
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        action = getMouseActionDown(mouse, event.button)
      elif event.type == pygame.MOUSEBUTTONUP:
        action = getMouseActionUp(mouse, event.button)

      if action == "click":
        value = handleClick(board, pygame.mouse.get_pos())
        try:
          numActive = numActive - value
        except TypeError:
          gameState = "lose"
      elif action == "mark":
        numBombsLeft = numBombsLeft + handleMark(board, pygame.mouse.get_pos())
      elif action == "double":
        value = handleDoubleClick(board, pygame.mouse.get_pos())
        try:
          numActive = numActive - value
        except TypeError:
          gameState = "lose"
    if numActive == 0:
      gameState = "win"
    # Update the display
    mouseSweep(mouse, pygame.mouse.get_pos(), board)
    currTime = timer.getTime()
    drawBoard(display, board, numBombsLeft, currTime)
    if gameState:
      break

  if gameState == "win":
    isWin = True
  else:
    isWin = False

  root = tk.Tk()
  EndScreen(root, isWin, bwidth, bheight, numBombs).grid()
  root.mainloop()
    
if __name__ == "__main__":
  # Call this before dialog box; it's faster
  pygame.init()

  # for i in pygame.font.get_fonts():
  #   print(i)
  
  # Game board icon logic
  pygame.display.set_caption("Minesweeper")
  pygame.display.set_icon(IMG_FLAG)

  # Menu initialization
  # Menu logic happens in the Menu class
  # Core game logic in the startGame() function (startGame called from the Menu class)
  root = tk.Tk()
  Menu(root).grid()
  root.mainloop()