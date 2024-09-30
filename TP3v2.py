from cmu_112_graphics import *
import random


###########################################
### Text
###########################################

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class TextField:
    def __init__(self, x, y, width, height=50, label=None, value=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.value = value
        
    def draw(self, canvas):
        canvas.create_text(self.x-self.width//2 - 5, self.y,
                           anchor='e', text=f'{self.label}:',fill="blue")
        canvas.create_rectangle(self.x - self.width//2, self.y - self.height//2,
                                self.x + self.width//2, self.y + self.height//2,
                                fill=None, outline = 'blue')
        if len(self.value):
            canvas.create_text(self.x, self.y, text=self.value, font = f'Arial {self.height//2}',fill='blue')
    def isFocused(self, x, y):
        return self.x - self.width //2 <= x <= self.x + self.width //2 and \
               self.y - self.height //2 <= y <= self.y + self.height // 2
        
class Button:
    def __init__(self, x, y, width, height, label=None):
        self.width = width
        self.height = height
        self.label = label
        self.x = x
        self.y = y
        self.focused = False
        self.hover = None
        self.textFill = 'blue'
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width//2, self.y - self.height//2,
                                self.x + self.width//2, self.y + self.height//2,
                                outline ="blue")
        if self.focused:
            self.hover = 'blue'
            self.textFill = 'white'
        canvas.create_rectangle(self.x - self.width//2, self.y - self.height//2,
                                self.x + self.width//2, self.y + self.height//2,
                                fill=self.hover, outline = 'blue')
        canvas.create_text(self.x, self.y, text=self.label,fill=self.textFill, font=f'Arial {self.width//10} bold')
    def isClicked(self, x, y):
        if self.x - self.width //2 <= x <= self.x + self.width //2 and \
               self.y - self.height //2 <= y <= self.y + self.height // 2:
            self.focused = True
        return self.x - self.width //2 <= x <= self.x + self.width //2 and \
               self.y - self.height //2 <= y <= self.y + self.height // 2
        
## Character -> PacMan -> Ghost
class Character:
    def __init__(self,x,y,row,col,r,state,color):
        self.color=color
        self.state = state
        self.row,self.col = row,col
        self.rows,self.cols = 20,15
        self.w,self.h = x,y
        self.r= r
        self.directionDict={'upright':(-1,+1),'downright':(+1,+1),'upleft':(-1,-1),'downleft':(+1,-1)}
        self.direction = self.directionDict['upright']
    def getPosition(self):
        return (self.row,self.col)
    def movePosition(self,newx,newy):
        self.row = newx
        self.col = newy
    def getDistance (self):
        x=self.w/self.cols*self.col
        y=self.h/self.rows*self.row
        return(x,y)
    def drawLogo(self,canvas):
        (a,b) = self.getDistance()
        if self.state == 0:
            canvas.create_oval(a-self.r,b-self.r,a+self.r,b+self.r,fill=self.color)
        else:
            canvas.create_oval(a-self.r,b-self.r,a+self.r,b+self.r,fill=self.color)
            canvas.create_arc(a-self.r,b-self.r,a+self.r,b+self.r,start=315,fill='black')

class PacMan (Character):
    def __init__(self,x,y,row,col,r,state,unit,color):
        super().__init__(x,y,row,col,r,state,color)
        self.x = x
        self.y = y
        self.unit = unit
        self.direction = (0,0)
        self.life = 1
    def getDistance(self):
        x=self.col*self.unit+0.5*self.unit
        y=self.row*self.unit+0.5*self.unit
        return (x,y)
    def getAngle(self):
        if self.direction == (-1,0): # down
            angle = 45
        elif self.direction == (+1,0): # up
            angle = 225
        elif self.direction == (0,+1): #right
            angle = 315
        else: # left
            angle = 135
        return angle
    def draw(self, canvas):
        (a,b)=self.getDistance()
        angle = self.getAngle()
        if self.state % 2 == 0:
            canvas.create_oval(self.x+a-self.r,self.y+b-self.r,self.x+a+self.r,self.y+b+self.r,fill=self.color)
        else:
            canvas.create_oval(self.x+a-self.r,self.y+b-self.r,self.x+a+self.r,self.y+b+self.r,fill=self.color)
            canvas.create_arc(self.x+a-self.r,self.y+b-self.r,a+self.x+self.r,self.y+b+self.r,start=angle,fill='black')

class Ghost (PacMan):
    def __init__(self,x,y,row,col,r,unit,color):
        super().__init__(x,y,row,col,r,0,unit,color)
        self.potentialDirections = [(-1, 0),(0, -1),(+1, 0),(0, +1)]
        self.direction = (-1,0)
    def draw(self,canvas):
        (a,b) = self.getDistance()
        canvas.create_oval(self.x+a-self.r,self.y+b-self.r,self.x+a+self.r,self.y+b+self.r,fill=self.color)
        canvas.create_oval(self.x+a-self.r//4-self.r//2,self.y+b-self.r//4,self.x+a+self.r//4-self.r//2,self.y+b+self.r//4,fill='white')
        canvas.create_oval(self.x+a-self.r//4,self.y+b-self.r//4,self.x+a+self.r//4,self.y+b+self.r//4,fill='white')        

class Mushroom(Ghost):
    def  __init__(self,x,y,row,col,r,unit,state,color,speed):
        super().__init__(x,y,row,col,r,unit,color)
        self.eaten = False
        self.speed = speed
        self.speed1 = 0
        self.eatenTime = 0
        self.score = 0
    def draw(self,canvas):
        (a,b) = self.getDistance()
        if self.state == 0 and self.eaten == False:
            canvas.create_oval(self.x+a-self.r+2,self.y+b-self.r+2,self.x+a+self.r-2,self.y+b+self.r-2,fill=self.color)
            canvas.create_rectangle(self.x+a-self.r+2,self.y+b-self.r+self.unit//2+2,self.x+a+self.r-2,self.y+b+self.r-2,fill='black')
            canvas.create_rectangle(self.x+a-self.r//2+2,self.y+b-self.r+self.unit//2+2,self.x+a+self.r//2-2,self.y+b+self.r-self.unit//4,fill=self.color)
        else:
            canvas.create_rectangle(self.x+a-self.r+2,self.y+b-self.r+2,self.x+a+self.r-2,self.y+b+self.r-2,fill='black')
    def drawEaten (self,canvas,x,y):
        if self.state == 0 and self.eaten == True:
            canvas.create_oval(x-self.r+2,y-self.r+2,x+self.r-2,y+self.r-2,fill=self.color)
            canvas.create_rectangle(x-self.r+2,y-self.r/+self.unit//2+2,x+self.r-2,y+self.r-2,fill='black')
            canvas.create_rectangle(x-self.r//2+2,y-self.r+self.unit//2+2,x+self.r//2-2,y+self.r-2-self.unit//4,fill=self.color)
        else:
            canvas.create_rectangle(x-self.r+2,y-self.r+2,x+self.r-2,y+self.r-2,fill='black')
        
class Maze (object):
    def __init__(self,list2D,level):
        self.maze = list2D
        self.level = level
        self.unit = 0
        self.rows=len(self.maze)
        self.cols=len(self.maze[0])
        self.port = 0
        self.x,self.y=0,0
    def getRowAndCol(self):
        return(self.rows,self.cols)
    def draw(self,canvas):    
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == "#":
                    if row==0 and 1<=col<self.cols-1: # Horizontal
                        canvas.create_line(self.x +col*self.unit,self.y+(row+1)*self.unit,
                                           self.x +(col+1)*self.unit,self.y+(row+1)*self.unit,fill="blue")
                    elif row == self.rows-1 and 1<=col<self.cols-1:
                        canvas.create_line(self.x+col*self.unit,self.y+row*self.unit,
                                            self.x+(col+1)*self.unit,self.y+row*self.unit,fill="blue")
                    elif col == 0 and 1<=row<self.rows-1: # Vertical
                        canvas.create_line(self.x+(col+1)*self.unit,self.y+row*self.unit,self.x+(col+1)*self.unit,self.y+(row+1)*self.unit,fill="blue")
                    elif col == self.cols-1 and 1<=row<self.rows-1:
                        canvas.create_line(self.x+col*self.unit,self.y+row*self.unit,self.x+col*self.unit,self.y+(row+1)*self.unit,fill="blue")
                elif self.maze[row][col] == "$":
                    if row%2==0: # Horizontal
                        canvas.create_rectangle(self.x+col*self.unit,self.y+row*self.unit,
                                                self.x+(col+1)*self.unit,self.y+(row+1)*self.unit,outline="blue")
                    else: #Vertical
                        canvas.create_rectangle(self.x+col*self.unit,self.y+row*self.unit,self.x+(col+1)*self.unit,self.y+(row+1)*self.unit,outline="blue")
                elif self.maze[row][col] == " ":
                    canvas.create_oval(self.x+(col+1/2)*self.unit-self.unit//10,self.y+(row+1/2)*self.unit-self.unit//10,
                                        self.x+(col+1/2)*self.unit+self.unit//10,self.y+(row+1/2)*self.unit+self.unit//10,fill="yellow")
                elif self.maze[row][col] == f"P{self.level}" or self.maze[row][col] == "U":
                    if self.port == 0:
                        canvas.create_line(self.x+col*self.unit,self.y+row*self.unit,self.x+col*self.unit,self.y+(row+1)*self.unit,fill='red')
                    else:    
                        canvas.create_line(self.x+col*self.unit,self.y+row*self.unit, self.x+(col+1)*self.unit,self.y+row*self.unit,fill='green')
                        canvas.create_line(self.x+(col+1)*self.unit,self.y+row*self.unit, self.x+(col+1)*self.unit,self.y+(row+1)*self.unit,fill='green')
                        canvas.create_line(self.x+col*self.unit,self.y+(row+1)*self.unit, self.x+(col+1)*self.unit,self.y+(row+1)*self.unit,fill='green')

#############################
## MODEL
#############################
def appStarted(app):
    app.count = 0
    app.focusedField = None
    app.logo = Character (app.width,app.height,5,6,app.width//20,0,'yellow')
    app.logo1 = Character(app.width,app.height,1,2,app.width//20,0,'orange')
    app.loginBtn = Button(app.width//2, app.height//4*3, 150, 50,  label="Login")
    app.username = TextField(app.width//2, app.height//2, 300, label="Username")
    app.gameState = 'login'    
    runGame(app)

# Run Pacman game (no login required)
def runGame(app):
    app.level0 = Button(app.width//7*1.5, app.height//3, app.width//7, app.height//3,  label="Level 1")
    app.level1 = Button(app.width//2, app.height//3, app.width//7, app.height//3,  label="Level 2")
    app.level2 = Button(app.width//7*5.5, app.height//3, app.width//7, app.height//3,  label="Level 3")
    app.levelOk = Button(app.width//2, app.height//3*2, 150, 50,  label="Start")
    app.unit = app.height//15
    app.timerDelay = 30
    app.score = 0
    app.lostImg = app.loadImage('cry.png')
    app.winImg = app.loadImage('Resize_pacman.webp')
    text='🙂😇🙃😉😊😀😃😄😁😆🤣😂'
    app.mazeDict = {0:[['#','#','#','#','#','#','#','#','#','#' ,'#','#','#','#','#','#','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ',' ',' ','$',' ','$','$','$',' ','$','$','$',' ','$',' ','#'],
                       ['#',' ',' ','$','$',' ',' ',' ','$',' ','$',' ',' ',' ','$',' ','#'], 
                       ['#',' ','$','+','$',' ',' ',' ','$',' ','$','$','$',' ','$',' ','#'], 
                       ['#',' ','$','$','$',' ','$','$','$',' ','$',' ','$',' ','$',' ','#'],
                       ['#',' ',' ',' ','$',' ','$',' ',' ',' ','$',' ',' ',' ','$',' ','#'],
                       ['#',' ',' ',' ','$',' ','$','$','$',' ','$','$','$',' ','$',' ','P0','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']],
                    1:[['#','#','#','#','#','#','#','#','#','#' ,'#','#','#','#','#','#','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ','$','$','$',' ','$','$','$',' ','$','$','$','$','$',' ','#'],
                       ['#',' ','$',' ','$',' ',' ',' ',' ',' ','$',' ','$',' ','$',' ','#'], 
                       ['#',' ','$',' ','$',' ',' ',' ',' ',' ','$',' ','$',' ','$',' ','#'], 
                       ['#',' ','$',' ','$',' ','$','$','$',' ','$',' ',' ',' ','$',' ','#'],
                       ['#',' ',' ',' ','$',' ','$','+','$',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ',' ',' ','$',' ','$','$','$',' ','$','$','$','$','$',' ','#'],
                       ['#',' ',' ','$','$',' ','$',' ',' ',' ','$',' ','$',' ',' ',' ','#'],
                       ['#',' ',' ','$',' ',' ','$',' ',' ',' ','$',' ','$',' ',' ',' ','#'],
                       ['#',' ',' ','$',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ',' ','$','$',' ',' ','$','$','$',' ',' ',' ',' ',' ',' ','P1','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','$','$',' ',' ',' ','#'],
                       ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']],
                    2:[['#','#','#','#','#','#','#','#','#','#' ,'#','#','#','#','#','#','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ','$',' ','$','$','$',' ','$',' ','$',' ','$','$','$',' ','#'],
                       ['#',' ','$',' ','$',' ',' ',' ','$',' ','$',' ',' ',' ','$',' ','#'], 
                       ['#',' ','$',' ','$','$','$',' ','$',' ','$',' ',' ',' ','$',' ','#'], 
                       ['#',' ','$',' ',' ',' ','$',' ','$',' ','$',' ','$','$','$',' ','U','#'],
                       ['#',' ','$',' ','$','$','$',' ','$',' ','$',' ','$',' ',' ',' ','#'],
                       ['#',' ','$',' ',' ',' ',' ',' ','$',' ','$',' ','$','$','$',' ','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ','$',' ',' ',' ','$',' ','$',' ',' ',' ','$',' ','$',' ','#'],
                       ['#',' ','$',' ',' ','$','$','$','$','$',' ',' ','$',' ','$',' ','#'],
                       ['#',' ','$',' ',' ','$','$','$','$','$',' ',' ','$',' ','$',' ','#'],
                       ['#',' ','$',' ',' ',' ','$','$','$',' ' ,' ',' ','$','$','$',' ','#'],
                       ['#',' ',' ',' ',' ',' ',' ','$',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
                       ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']],
                }
    app.level = 0
    app.regenerate = 0
    app.regenerated = False
    initGame(app)
    
# Drawn each level
def initGame(app):
    app.maze = Maze(app.mazeDict[app.level],app.level)
    app.maze.unit=app.unit
    app.x,app.y=(app.width-app.maze.unit*app.maze.cols)/2, (app.height-app.maze.unit*app.maze.rows)/2
    r = app.unit//2
    app.maze.x,app.maze.y=app.x,app.y
    if app.level == 0:
        app.pacMan = PacMan(app.x,app.y,6,2,r,0,app.unit,'yellow')
        app.ghost = Ghost(app.x,app.y,1,10,r,app.unit,'red')
        app.mushRoom = Mushroom(app.x,app.y,6,12,r,app.unit,0,rgbString(171,32,253),0)
        app.mushRoom1 = Mushroom(app.x,app.y,3,12,r,app.unit,0,'white',0)
        app.life = Mushroom(app.x,app.y,3,7,r,app.unit,0,'green',0)
    elif app.level == 1:
        app.pacMan = PacMan(app.x,app.y,1,1,r,0,app.unit,'yellow')
        app.ghost = Ghost(app.x,app.y,10,1,r,app.unit,'red')
        app.ghost1 = Ghost(app.x,app.y,3,11,r,app.unit,'pink')
        app.life = Mushroom(app.x,app.y,3,5,r,app.unit,0,'green',0)
        app.mushRoom = Mushroom(app.x,app.y,4,3,r,app.unit,0,'white',0)
        app.mushRoom1 = Mushroom(app.x,app.y,5,11,r,app.unit,0,rgbString(171,32,253),0)
    elif app.level == 2:
        app.pacMan = PacMan(app.x,app.y,1,1,r,0,app.unit,'yellow')
        app.ghost = Ghost(app.x,app.y,10,1,r,app.unit,'red')
        app.ghost1 = Ghost(app.x,app.y,3,11,r,app.unit,'blue')
        app.mushRoom = Mushroom(app.x,app.y,9,7,r,app.unit,0,'white',0)
        app.mushRoom1 = Mushroom(app.x,app.y,9,13,r,app.unit,0,rgbString(171,32,253),0)
        app.life = Mushroom(app.x,app.y,3,5,r,app.unit,0,'green',0)
    app.rows,app.cols= app.maze.getRowAndCol()
    app.pacMan.direction = (0,0)
    app.score = 0
    app.count = 0
 

#############################
## CONTROLLER
#############################

# Draw Logo at the beginning & end
def checkPositionLogo(app,logo):
    (row,col) = logo.getPosition()
    (x,y) = logo.getDistance()
    if  x - logo.r <= 0: # Hit left from down
        if  logo.direction ==  logo.directionDict['upleft']:
            logo.direction =  logo.directionDict['upright']
        else: # Hit left from up
            logo.direction =  logo.directionDict['downright']
    elif  x + logo.r>=app.width: # Hit right from up
        if  logo.direction ==  logo.directionDict['downright']:
            logo.direction =  logo.directionDict['downleft']
        else:  # Hit right from down
            logo.direction =  logo.directionDict['upleft']
    elif  y - logo.r<=0: # Hit top from left
        if  logo.direction ==  logo.directionDict['upleft']:
            logo.direction =  logo.directionDict['downleft']
        else: # Hit top from right
            logo.direction =  logo.directionDict['downright']
    elif y + logo.r>=app.height: # Hit down from left
        if  logo.direction ==  logo.directionDict['downleft']:
            logo.direction =  logo.directionDict['upleft']
        else: # Hit down from right
            logo.direction =  logo.directionDict['upright']
    (drow,dcol) =  logo.direction
    (newRow,newCol) = (row+drow,col+dcol)
    logo.movePosition(newRow,newCol)


# Intro - use to take username - and choose level
def mousePressed(app, event):
    # Input user
    if app.gameState == 'login':
        if app.username.isFocused(event.x, event.y):
            app.username.focused = True
        else:
            app.username.focused = False
        if app.loginBtn.isClicked(event.x, event.y) and app.username.value != '':
                app.gameState = "waiting"
                app.username = app.username.value
    # Choose level
    if app.gameState == "waiting":
        if (0<event.x<app.width) and (0<event.y<app.height):
            app.gameState = "chooseLevel"
    if app.gameState == 'chooseLevel':
        if app.level0.isClicked(event.x, event.y):
            app.level = 0
            app.level1.hover,app.level1.focused,app.level1.textFill = None,False,'blue'
            app.level2.hover,app.level2.focused,app.level2.textFill = None,False,'blue'
        elif app.level1.isClicked(event.x, event.y):
            app.level = 1
            app.level0.hover,app.level0.focused,app.level0.textFill = None,False,'blue'
            app.level2.hover,app.level2.focused,app.level2.textFill = None,False,'blue'
        elif app.level2.isClicked(event.x, event.y):
            app.level = 2
            app.level0.hover,app.level0.focused,app.level0.textFill = None,False,'blue'
            app.level1.hover,app.level1.focused,app.level1.textFill = None,False,'blue'
        if app.level0.focused == True or app.level1.focused == True or app.level2.focused == True:    
            app.levelOk.isClicked(event.x, event.y)
            if app.levelOk.focused == True:
                initGame(app)
                app.gameState = "playing"

def keyPressed(app, event):
    # Take Username
    if app.gameState == 'login':
        if isinstance(app.username,TextField):
            if event.key =="Backspace":
                app.username.value=app.username.value[:len(app.username.value)-1]
            if len(event.key)==1 and event.key.isalpha() and len(app.username.value) < 15:
                app.username.value += event.key
            if event.key == "Enter" and len(app.username.value)>0:
                app.gameState = "waiting"
                app.username = app.username.value
    # Start Game
    elif app.gameState == 'chooseLevel':
        if event.key == "Enter":
            initGame(app)
            app.gameState = "playing"
    elif app.gameState =="playing": # Change Character Direction
        if (event.key == 'Up'):      app.pacMan.direction = (-1, 0) 
        elif (event.key == 'Down'):  app.pacMan.direction = (+1, 0)
        elif (event.key == 'Left'):  app.pacMan.direction = (0, -1)
        elif (event.key == 'Right'): app.pacMan.direction = (0, +1)
    elif app.gameState == "gameOver":
        if event.key == 'r': # play again
            app.gameState = 'chooseLevel'
            app.levelOk.focused = False
            runGame(app)
    if app.gameState == 'win': # play again
        if event.key == 's':
            app.gameState = 'chooseLevel'
            runGame(app)

# Helper function for playerBooster
def eatMushRoom(app,mushRoom,speed):
    if app.pacMan.getPosition() == mushRoom.getPosition() and mushRoom.eaten == False:
        mushRoom.speed = speed
        app.pacMan.direction = (0,0)
        app.pacMan.color = mushRoom.color
        mushRoom.eaten = True
        mushRoom.eatenTime = app.count
    if mushRoom.eaten == True and 70<app.count-mushRoom.eatenTime:
        app.pacMan.color = 'yellow'
        mushRoom.speed = 0
        
# Call when the player eat the mushroom
def playerBooster(app):
    if app.mushRoom.color=='white'and app.mushRoom1.eaten == False:
        eatMushRoom(app,app.mushRoom,-3)
    elif app.mushRoom1.eaten == False:
        eatMushRoom(app,app.mushRoom,2)
    if app.mushRoom.eaten == True and 100<app.count-app.mushRoom.eatenTime:
        if app.mushRoom1.color =='white':
            eatMushRoom(app,app.mushRoom1,-3)
        else:
            eatMushRoom(app,app.mushRoom1, 2)

# Pacman character Move ↑ ↓ ← → and eat food
def takeStep(app):
    (drow, dcol) = app.pacMan.direction
    (oldRow, oldCol) = app.pacMan.getPosition()
    (newRow, newCol) = (oldRow+drow, oldCol+dcol)
    if not any(' ' in nested_list for nested_list in app.maze.maze):
        app.maze.port=1
        if app.maze.maze[newRow][newCol]== f"P{app.level}" or  app.maze.maze[newRow][newCol]== "U":
            app.pacMan.movePosition(newRow,newCol)
        if app.maze.maze[oldRow][oldCol]== "U":
            app.gameState = "win"
        if app.maze.maze[oldRow][oldCol]== f"P{app.level}":
            app.gameState = "win"
    if ((newRow < 0) or (newRow >= app.rows) or
        (newCol < 0) or (newCol >= app.cols) or
        (app.maze.maze[newRow][newCol]!=' ') and
        (app.maze.maze[newRow][newCol]!='-') and
        (app.maze.maze[newRow][newCol]!='s')):
        app.pacMan.direction = (0,0)
    else:
        if app.maze.maze[oldRow][oldCol] == ' ':
            app.score+=1 # Update score
        app.maze.maze[oldRow][oldCol]='-' # change map and move pacMan
        app.pacMan.movePosition(newRow,newCol)
        
# Call when a user eaten a green mushroom and have 1 chance 
def gainLife (app):
    if app.pacMan.getPosition() == app.life.getPosition() and app.life.eaten == False:
        app.pacMan.life += 1
        app.life.eaten = True

# Helper function for ghostHaunt        
def checkSameCol(app, ghost):
    (pmRow,pmCol) = app.pacMan.getPosition() 
    (oldRow, oldCol) = ghost.getPosition()
    deltaRow = pmRow - oldRow
    if deltaRow < 0:
        for i in range(pmRow,oldRow):
            if app.maze.maze[i][pmCol] == '$':
                return  ghost.direction # app.ghost.direction
        return (-1,0)
    if deltaRow > 0:
        for i in range(oldRow,pmRow):
            if app.maze.maze[i][pmCol] == '$':
                return ghost.direction
        return (+1,0)

# Ghost move on its own to catch the user
def ghostHaunt(app,ghost):
    (pmRow,pmCol) = app.pacMan.getPosition() 
    (oldRow, oldCol) = ghost.getPosition()
    if (pmRow,pmCol) == (oldRow, oldCol):
        app.gameState="gameOver"
    elif pmRow == oldRow and oldCol < pmCol and '$' not in app.maze.maze[oldRow][oldCol:pmCol] :
        ghost.direction = (0,+1)
    elif pmRow == oldRow and pmCol < oldCol and '$' not in app.maze.maze[oldRow][pmCol:oldCol]:
        ghost.direction = (0,-1)
    elif pmCol == (oldCol):
        ghost.direction = checkSameCol(app,ghost)
    (drow,dcol) = ghost.direction
    (newRow, newCol) = (oldRow+drow, oldCol+dcol)
    if (newRow, newCol)==app.pacMan.getPosition():  
        ghost.movePosition(newRow,newCol)
        app.pacMan.life -= 1
        if app.pacMan.life==0:
            app.gameState = "gameOver"
        else: 
            app.gameState = 'regenerating'
    if ((app.maze.maze[newRow][newCol]!='#')and
        (app.maze.maze[newRow][newCol]!='$')): 
        ghost.movePosition(newRow,newCol)    
    elif ((app.maze.maze[newRow][newCol]=='#')or
          (app.maze.maze[newRow][newCol]=='$')):
        ghost.direction = app.ghost.potentialDirections[random.randint(0, len(app.ghost.potentialDirections)-1)]

# Call at the beginning and every waiting screen for 2 Pacman moving diagonally
def timerLogoAnimation(app):
    if app.gameState == 'login' or app.gameState == 'waiting' or app.gameState == 'chooseLevel':
        app.count += 1 
        if app.count % 5 == 0:
            # Resizing 
            if app.gameState =='login':
                app.username.x,app.username.y=app.width//2,app.height//2
                app.loginBtn.x,app.loginBtn.y=app.width//2,app.height//4*3
            if app.gameState == 'chooseLevel':
                app.level0.x,app.level0.y = app.width//7*1.5, app.height//3
                app.level1.x,app.level1.y = app.width//2, app.height//3
                app.level2.x,app.level2.y = app.width//7*5.5, app.height//3
                app.levelOk.x,app.levelOk.y = app.width//2, app.height//3*2
            checkPositionLogo(app,app.logo)
            checkPositionLogo(app,app.logo1)
            app.logo.state = 1-app.logo.state
            app.logo1.state = 1-app.logo1.state

# Call when a user eaten a green mushroom and have 1 chance 
def regeneratingAnimation(app):
    if app.gameState == 'regenerating':
        if app.count % 15 == 0 and app.regenerate <= 4:
            app.regenerate +=1
        if app.regenerate == 4:
            app.regenerate = 0
            app.gameState='playing'
            app.regenerated = True
            initGame(app)
            

def timerFired(app):
    timerLogoAnimation(app)
    if app.gameState!="playing" and app.gameState!='regenerating': return
    regeneratingAnimation(app)
    app.count += 1 
    if app.count % 7 == 0:  
        app.pacMan.state = 1 - app.pacMan.state
        app.mushRoom.state = 1 - app.mushRoom.state
        app.mushRoom1.state = 1 - app.mushRoom1.state
        app.life.state = 1 - app.life.state
    if app.count % (5+app.mushRoom.speed+app.mushRoom1.speed) == 0:
        takeStep(app)
        playerBooster(app)
        gainLife(app)
    if app.count % 7 == 0 and app.gameState == 'playing':
        if app.level==0:
            ghostHaunt(app,app.ghost) 
        else:
            ghostHaunt(app,app.ghost)
            ghostHaunt(app,app.ghost1) 
            app.ghost1.x,app.ghost1.y = app.x,app.y
        app.x,app.y = (app.width-app.maze.unit*app.maze.cols)/2, (app.height-app.maze.unit*app.maze.rows)/2
        app.maze.x,app.maze.y = app.x,app.y
        app.pacMan.x,app.pacMan.y = app.x,app.y
        app.ghost.x,app.ghost.y = app.x,app.y
        app.mushRoom.x,app.mushRoom.y = app.x,app.y
        app.mushRoom1.x,app.mushRoom1.y = app.x,app.y
        app.life.x,app.life.y = app.x,app.y

#############################
## VIEW
#############################
def drawLogin(app, canvas):
    if app.gameState == 'login':
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        app.logo.drawLogo(canvas)
        app.logo1.drawLogo(canvas)
        app.username.draw(canvas)
        app.loginBtn.draw(canvas)
        canvas.create_text(app.width//2,app.height//4,text="Welcome to The Pacman Maze Survivor",font=f"Arial {app.unit//3*2} bold",fill="green",anchor ='s')
        canvas.create_text(app.width//2,app.height//4,text="Input your name",font=f"Arial {app.unit//3*2}",fill="blue",anchor = 'n')
        canvas.create_image(app.width,app.height, anchor = "se",image=ImageTk.PhotoImage(app.winImg))

def drawGameStart(app,canvas):
    if app.gameState== "waiting":
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        app.logo.drawLogo(canvas)
        app.logo1.drawLogo(canvas)
        canvas.create_text(app.width//2,app.height//8,text = 'Game Rules', font=f"Arial {app.unit}",fill='red')
        canvas.create_text(app.width//2,app.height//8*3,text="You can move ↑ ↓ ← → to eat the food\nThe ghosts will find and catch you",
                           font=f"Arial {app.unit//3} bold",fill='blue')
        canvas.create_text(app.width//2,app.height//8*4,text="If you're caught, game over!",
                           font=f"Arial {app.unit//3} bold",fill='blue')
        canvas.create_text(app.width//2,app.height//8*5,text="There will be some mushrooms to help or harm you,\nTutorial is in level 1",
                           font=f"Arial {app.unit//3} bold",fill='blue')
        canvas.create_text(app.width//2,app.height//8*6,text="When finish, the gate at the end of the map will open\nIt will be closed until all food is eaten",
                           font=f"Arial {app.unit//3} bold",fill='green')
        canvas.create_text(app.width//2,app.height//8*7,text="(Click anywhere on the screen to start)",
                           font=f"Arial {app.unit//3} bold",fill='white')
        canvas.create_image(app.width,app.height, anchor = "se",image=ImageTk.PhotoImage(app.winImg))
        
def drawChooseLevel(app,canvas):
    if app.gameState == 'chooseLevel':
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        app.logo.drawLogo(canvas)
        app.level0.draw(canvas)
        app.level1.draw(canvas)
        app.level2.draw(canvas)
        app.levelOk.draw(canvas)

# Helper for drawLevel0,drawLevel
def drawMushroom(app,canvas):
    if app.score>10:
        app.mushRoom.draw(canvas)
        if app.mushRoom.eaten == False:
            canvas.create_text(app.width//2,app.maze.y,text="Purple mushroom unlocked",fill = rgbString(171,32,253),font = f"Arial {app.unit//2}",anchor ='s' )
        elif app.mushRoom.eaten == True:
            if app.count-app.mushRoom.eatenTime <= 100:
                canvas.create_text(app.width//2,app.maze.y,text="Purple mushroom slows you down",fill = rgbString(171,32,253),font = f"Arial {app.unit//2}",anchor ='s' )
            app.mushRoom.drawEaten(canvas,app.maze.x+app.maze.unit,app.maze.y+app.maze.rows*app.maze.unit)
    if app.mushRoom.eaten==True and 100 < app.count-app.mushRoom.eatenTime:
        app.mushRoom1.draw(canvas)
        if app.mushRoom1.eaten == False:
            canvas.create_text(app.width//2,app.maze.y,text="White mushroom unlocked",fill = "white",font = f"Arial {app.unit//2}",anchor ='s')
        elif app.mushRoom1.eaten == True:
            if app.count-app.mushRoom1.eatenTime <= 100 :
                canvas.create_text(app.width//2,app.maze.y,text="White mushroom speeds you up",fill = "white",font = f"Arial {app.unit//2}",anchor ='s')
            app.mushRoom1.drawEaten(canvas,app.maze.x+2*app.maze.unit,app.maze.y+app.maze.rows*app.maze.unit)
    if app.mushRoom1.eaten == True and 100<app.count-app.mushRoom1.eatenTime <= 1000:
        app.life.draw(canvas)
        if app.life.eaten == False:
            canvas.create_text(app.width//2,app.maze.y,text="Green mushroom unlocked",fill = "green",font = f"Arial {app.unit//2}",anchor ='s')
        elif app.life.eaten == True:
            canvas.create_text(app.width//2,app.maze.y,text="Green mushroom give 1 extra life",fill ="green",font = f"Arial {app.unit//2}",anchor ='s')
            app.life.drawEaten(canvas,app.maze.x+3*app.maze.unit,app.maze.y+app.maze.rows*app.maze.unit)

# Helper for drawMaze
def drawLevel0(app,canvas):
    if app.level == 0:    
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        canvas.create_text(app.maze.x+app.maze.unit*app.maze.cols,app.maze.y,text=f'Score: {app.score}',anchor="ne",font=f'LaTeX {app.unit//2}', fill='blue')
        app.maze.draw(canvas)
        drawMushroom(app,canvas)
        app.pacMan.draw(canvas)
        app.ghost.draw(canvas)
                
# Helper for drawMaze
def drawLevel(app,canvas,level):
    if app.level == level:    
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        canvas.create_text(app.maze.x+app.maze.unit*app.maze.cols,app.maze.y,text=f'Score: {app.score}',anchor="ne",font=f'LaTeX {app.unit//2}', fill='blue')
        app.maze.draw(canvas)
        if app.life.eaten == False and app.regenerated == False:
            app.life.draw(canvas)
        elif app.regenerated == False:
            app.life.drawEaten(canvas,app.maze.x+app.maze.unit,app.maze.y+app.maze.rows*app.maze.unit)
        if  app.mushRoom.eaten==False and app.score > 10:
            app.mushRoom.draw(canvas)
        elif app.mushRoom.eaten==True:
            if 100 < app.count-app.mushRoom.eatenTime:
                app.mushRoom1.draw(canvas)
        app.pacMan.draw(canvas)
        app.ghost.draw(canvas)
        app.ghost1.draw(canvas)

# Draw when a user eaten a green mushroom and have 1 chance 
def drawRegenerating(app,canvas):
    if app.gameState == 'regenerating':
        canvas.create_rectangle(0,0,app.width,app.height,fill='black')
        canvas.create_text(app.width//2,app.height//3,text='Regenerate In', font = f"Arial {app.unit} bold",fill='blue')
        canvas.create_text(app.width//2,app.height//3*2,text=f'{4-app.regenerate}',font = f"Arial {app.unit} bold",fill='blue')

# Draw All level
def drawMaze(app,canvas):
    drawRegenerating(app,canvas)
    if app.gameState == "playing":
        drawLevel0(app,canvas)
        drawLevel(app,canvas,1)
        drawLevel(app,canvas,2)

def drawGameOver(app,canvas):
    if app.gameState == "gameOver":
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        canvas.create_text(app.width//2,app.height//3,text=f"Game Over!",font=f"Arial {app.unit} bold",fill="red",anchor="s")
        canvas.create_text(app.width//2,app.height//2,text="Press R to Restart!",font=f"Arial {app.unit} bold",fill="blue",anchor="s")
        canvas.create_image(app.width//2,app.height//3*2,image=ImageTk.PhotoImage(app.lostImg))

# Helper for Draw Game Won
def drawFractalPacMan (app,canvas,x):
    if x == app.width:
        return
    else:
        canvas.create_oval(x-app.width//20,app.height//2-app.width//20,x+app.width//20,app.height//2+app.width//20,fill='yellow')
        canvas.create_arc(x-app.width//20,app.height//2-app.width//20,x+app.width//20,app.height//2+app.width//20,start=315,fill='black')
        drawFractalPacMan (app,canvas,x+app.width//10)

def drawGameWon (app,canvas):
    if app.gameState == "win":
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
        drawFractalPacMan(app,canvas,app.width//10)
        canvas.create_text(app.width//2,app.height//3,text=f"You Won! Congratulation {app.username.upper()}",font=f"Arial {app.unit} bold",fill="red",anchor="s")
        canvas.create_text(app.width//2,app.height//3*2,text=f"Press S to Play Again",font=f"Arial {app.unit} bold",fill="blue",anchor="n")

def redrawAll(app,canvas):
    drawLogin(app,canvas)
    drawGameStart(app,canvas)
    drawChooseLevel(app,canvas)
    drawMaze(app,canvas)
    drawGameWon(app,canvas)
    drawGameOver(app,canvas)

runApp(width=800,height=500)