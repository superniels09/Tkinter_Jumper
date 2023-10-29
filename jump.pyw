import tkinter as tk
import math
import random
import time
import json

colors = json.load(open("colors.json"))
deaths = json.load(open("deaths.json"))

root = tk.Tk()

canvas = tk.Canvas(width=600,height=800,bg="#ADD8E6")
root.title("Jump.py")
canvas.pack()

platforms = []
hitboxes = []

left = False
right = False
up = False

def on_left_arrow_press(event):
    global left
    left = True

def on_left_arrow_release(event):
    global left
    left = False


root.bind("<Left>", on_left_arrow_press)
root.bind("<KeyRelease-Left>", on_left_arrow_release)

def on_right_arrow_press(event):
    global right
    right = True

def on_right_arrow_release(event):
    global right
    right = False


root.bind("<Right>", on_right_arrow_press)
root.bind("<KeyRelease-Right>", on_right_arrow_release)

def on_space_press(event):
    global InGame, vx, vy, playerX, playerY, camvY, camX, camY, platforms, jump, superjump, score, heightDensity, level, offset, AccentColor, noGrav, Controls
    if not InGame:
        canvas.config(bg="#ADD8E6")
        root.config(bg="#ADD8E6")

        InGame = True
        vx, vy = 0,0
        playerX,playerY = 0, 200

        camvY = 0
        camX = 0
        camY = 0

        jump = 0
        superjump = 0

        score = 0
        heightDensity = 70
        level = 0
        AccentColor = "white"

        offset = 0
        noGrav = 30

        Controls = True

        platforms = []
        initPlatforms()

def on_up_press(event):
    global up
    up = True

def on_up_release(event):
    global up
    up = False

root.bind("<space>", on_space_press)

root.bind("<Up>", on_up_press)
root.bind("<KeyRelease-Up>", on_up_release)

def calcRel(x,y):
    relX = x - camX
    relX = math.remainder(relX,800) + 300

    relY = y + camY
    return relX, relY

def drawPlatforms():
    global platforms, hitboxes
    hitboxes = []

    for id, platform in enumerate(platforms):
        x = platform[0]
        y = platform[1]
        Ptype = platform[2]

        relX, relY = calcRel(x,y)

        platform_width = 60
        platform_height = 10

        cords = [relX-platform_width,relY-platform_height,relX+platform_width,relY+platform_height]
        color = AccentColor

        if platform[2] == 1:
            if random.randint(0,1):
                outline = "aqua"
            else:
                outline = "lime"
        elif platform[2] == 2:
            outline = "#07d100" #greenish color
            color = "green"
        elif platform[2] == 3:
            if random.randint(0,1):
                outline = "yellow"
            else:
                outline = "gold"
            color = "#ffd20a"
        else:
            outline = "black"

        canvas.create_rectangle(cords,fill=color,outline=outline,width=5)
        hitboxes.append([cords, platform[2]])

        if relY > 900:
            platforms.pop(id)

            if random.randint(0,10) == 0:
                Ptype = 2
            elif random.randint(0,20) == 0:
                Ptype = 1
            elif random.randint(0,40) == 0:
                Ptype = 3
            else:
                Ptype = 0

            platforms.append([random.randint(0,600),-100 - camY + random.randint(0-offset,offset),Ptype])

def initPlatforms():
    global platforms
    for y in range(round(900/heightDensity)):
        platforms.append([random.randint(0,800),y*heightDensity,0])

def drawPlayer(x,y):
    global PrelX, PrelY
    PrelX, PrelY = calcRel(x,y)

    if superjump > 0:
        if random.randint(0,1) == 0:
            color = "aqua"
        else:
            color = "lime"
    elif noGrav > 0:
        color = "blue"
    else:
        color = AccentColor

    canvas.create_rectangle(PrelX-playerSize,PrelY-playerSize,PrelX+playerSize,PrelY+playerSize,fill=color,outline="black",width=5)

def inBox(cords,box):
    x,y = cords[0], cords[1]

    xA, yA = box[0], box[1]
    xB, yB = box[2], box[3]

    return (x > xA and x < xB) and (y > yA and y < yB)

def handleJump():
    global playerX, playerY, vx, vy, Controls, jump, superjump, noGrav, deaths

    if not Controls:
        vy -= 2.5
        return

    if up and not superjump > 0:
        jump = 25
        superjump = 75

    collision = False
    for hitbox in hitboxes:
        cordsLeft = calcRel(playerX - playerSize, playerY + playerSize)
        cordsRight = calcRel(playerX + playerSize, playerY + playerSize)

        if not jump > 0:
            if inBox(cordsLeft,hitbox[0]) or inBox(cordsRight,hitbox[0]) or cordsLeft[1] > 800:
                if not jump > 0:
                    if hitbox[1] == 1:
                        jump = 30
                        noGrav = 60
                    elif hitbox[1] == 2:
                        noGrav = 10
                        vx = 0
                        vy = -1
                    elif hitbox[1] == 3:
                        jump = 90
                        noGrav = 180
                    else:
                        jump = 18
                
                collision = True

                if cordsLeft[1] > 800:
                    if score > 120:
                        Controls = False
                        deaths.append([playerX,playerY,round(score)])
                        json.dump(deaths,open("deaths.json","w"))
                    else:
                        jump = 18

                break

    if (not collision) and (not noGrav > 0):
        vy -= 2.5
    else:
        if noGrav > 0:
            noGrav -= 1
    
    if jump > 0:
        jump -= 1

        if jump > 8:
            vy += 10
    
    if superjump > 0:
        superjump -= 1


def movePlayer():
    global playerX, playerY, vx, vy
    
    handleJump()

    if Controls:
        if left:
            vx -= 4

        if right:
            vx += 4

    vx *= 0.85
    vy *= 0.85

    playerX += vx
    playerY -= vy

def moveCam():
    global camX, camY, camvY

    camX -= (camX - playerX) / 5

    relX, relY = calcRel(playerX,playerY)

    if relY < 300:
        camvY += 2
    else:
        camvY *= 0.8

    if not Controls:
        camvY -= 4
    

    camY += camvY

def newLevel(level):
    global canvas, heightDensity, platforms, superjump, AccentColor

    data = colors[str(level)]

    canvas.config(bg=data[0])
    root.config(bg=data[0])
    AccentColor = data[1]
    offset = data[2]
    

def updateLevel():
    global level

    for i in range(1,len(colors)):
        if score > (1000 + (2000*(i-1))) and level == (i-1):
            level = i
            newLevel(level)

def DeathScreen():
    canvas.create_text(300,(100+(math.cos(tick/30)*8)), text="Jump.py", fill=AccentColor, font=("Helvetica", 80))
    canvas.create_text(300,(300+(math.sin(tick/30)*8)), text="Press Space", fill=AccentColor, font=("Helvetica", 50))
    root.title("Jump.py")

def drawScore():
    global score
    score = camY / 4
    scoreStr = "Score: "+str(round(score))

    scoreX, y = calcRel(0,0)
    scoreY = (math.remainder((40+camY),2000)) + 1000

    floatScoreString = str(round(score))


    canvas.create_text(scoreX,scoreY,text=floatScoreString, fill=AccentColor, font=("Helvetica", 20))

    canvas.create_line(-800,scoreY+20,800,scoreY+20,fill=AccentColor, width=5)

    root.title("Jump.py - "+scoreStr+" , Level: "+str(level))

def drawBackground():
    for y in range(0,25):
        ypos = math.remainder((y*40 + camY),1000) + 500
        canvas.create_line(-800,ypos,800,ypos,fill=AccentColor)

def drawDeaths():
    for death in deaths:
        x,y = calcRel(death[0],death[1])
        
        if y > -10 and y < 810:
            if death[2] < score:
                color = "green"
            else:
                color = "red"

            canvas.create_line(x-50,y,x+50,y,fill=color,width=5)
            canvas.create_text(x,y-20,fill=color,text=str(death[2]))

vx, vy = 0,0
playerX,playerY = 0, 200
playerSize = 30

camX = 0
camY = 0

camvY = 0
InGame = False
tick = 0
jump = 0
superjump = 0
score = 0
heightDensity = 70
level = 0
AccentColor = "white"

PrelX, PrelY = 0,0

Controls = False

offset = 0
noGrav = 30

initPlatforms()

#main loop
while True:
    try:
        canvas.delete('all')
    except:
        exit()
    
    movePlayer()
    moveCam()

    drawBackground()
    if InGame:
        drawScore()
    drawDeaths()

    drawPlatforms()

    updateLevel()

    drawPlayer(playerX,playerY)

    if not Controls:
        InGame = False
        DeathScreen()


    root.update()
    tick += 1

    time.sleep(0.01)