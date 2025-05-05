from turtle import Screen
import time, snakesUtil as su

# Setting up display screen
SCREEN = Screen()
SCREEN.setup(600,600)
SCREEN.bgcolor("black")
SCREEN.tracer(0) #tracer is usedto live track turtle movements, but we're switching it off
# Essentially we're just updating different snapshots of the state of the SCREEN frequently to show a live motion. Otherwise if the live tracer is on the motion will seem weird movement break break kore hobe

# Setting up the Score turtle and score counter
SCORE = 0
SNAKE_SCORE_TURTLE = su.Score(SCORE)
SEGMENTS = list()

# Setting up the food turtle
snakeFood = su.Food()
snakeFood.rand_pos()

# Creating a 3 turtle segment snake to start with
init_poses = [(-20.0,0.0),(0.0,0.0),(20.0,0.0)]
COUNT = 1 # Keeps a count of the number of segments of snek

for pos in init_poses:
    seg = su.Snakes(COUNT)
    seg.setpos(pos)
    SEGMENTS.append(seg)
    COUNT += 1
    print(seg)

# Keeps the snake moving in 1 direction
def shift():
    global SEGMENTS
    for i in range(0,len(SEGMENTS)-1):
        SEGMENTS[i].setpos(SEGMENTS[i+1].pos())
    SEGMENTS[-1].forward(20)
    return

# Called upon gulping food, adds a seg to snek
def add_seg():
    global SEGMENTS
    global COUNT
    new_seg = su.Snakes(COUNT)
    COUNT += 1
    # print(new_seg)
    new_seg.setpos(SEGMENTS[0].pos())
    shift()
    SEGMENTS.reverse()
    SEGMENTS.append(new_seg)
    SEGMENTS.reverse()
    return

# on key up
def up():
    global SEGMENTS
    head = SEGMENTS[-1].heading()
    seg = SEGMENTS[-1]

    if head == 180.0:
        seg.right(90)    
    elif head == 0.0:
        seg.left(90)
    else:
        pass
    
    return

# On key down  
def down():
    global SEGMENTS
    head = SEGMENTS[-1].heading()
    seg = SEGMENTS[-1]
    if head == 0.0:
        seg.right(90)    
    elif head == 180.0:
        seg.left(90)
    else:
        pass

    return

# on key left
def left():
    global SEGMENTS
    head = SEGMENTS[-1].heading()
    seg = SEGMENTS[-1]
    
    if head == 90.0:
        seg.left(90)    
    elif head == 270.0:
        seg.right(90)
    else:
        pass
    
    return

# on key right
def right():
    global SEGMENTS
    head = SEGMENTS[-1].heading()
    seg = SEGMENTS[-1]

    if head == 90.0:
        seg.right(90)
    elif head == 270.0:
        seg.left(90)
    else: 
        pass

    return

# shows the final screen upon gameover, using the score turtle
def gameOver():
    global SNAKE_SCORE_TURTLE
    global SCORE
    SNAKE_SCORE_TURTLE.setpos(0,0)
    SNAKE_SCORE_TURTLE.refreshScore(SCORE, "Game Over!\nFinal Score")
    return

# first update of screen
SCREEN.update()

# event listeners
SCREEN.listen()
SCREEN.onkey(up,"Up")    
SCREEN.onkey(down,"Down")
SCREEN.onkey(left,"Left")
SCREEN.onkey(right,"Right")


# Main event loop
gameOn = True
while gameOn:
    shift()
    time.sleep(0.08) #using sleep to delay the otherwise too fast updates
    SCREEN.update()

    # Condition to check food gulp
    if SEGMENTS[-1].distance(snakeFood) < 15:
        snakeFood.rand_pos()
        add_seg()
        SCORE += 1
        SNAKE_SCORE_TURTLE.refreshScore(SCORE)
    
    # Condition to check screen wall collision
    head = SEGMENTS[-1]
    if head.xcor() > 300.0 or head.xcor() < -300.0 or head.ycor() > 300.0 or head.ycor() < -300.0:
        gameOver()
        gameOn = False

    # Condition to check self bite
    for seg in SEGMENTS[:len(SEGMENTS)-1]:
        if seg.distance(head) < 5:
            gameOver()
            gameOn = False
            break
        
    
SCREEN.update() # Last scren update to show the game over screen
SCREEN.exitonclick() #Keeps the SCREEN on/doesnt kill the SCREEN until we click
