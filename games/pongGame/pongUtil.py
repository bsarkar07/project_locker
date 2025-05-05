import turtle as t

class PongScreen():
    
    def __init__(self):
        self.screen = t.Screen()
        self.screen.setup(800, 600)
        self.screen.bgcolor("black")
        self.screen.tracer(0)

class PongPaddle(t.Turtle):
    
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len = 4, stretch_wid = 1)
        self.left(90)
        self.score = 0

    def up(self):
        if self.ycor() >= 250:
            pass
        else:
            head = self.heading()
            if head == 270.0:
                self.left(180)
            self.forward(20)

    def down(self):
        if self.ycor() <= -250:
            pass
        else:
            head = self.heading()
            if head  ==  90:
                self.left(180)
            self.forward(20)

class Score(t.Turtle):
    
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.hideturtle()
        
    def refreshScore(self, text):
        self.clear()
        self.write(text, align = "center", font = ("Arial", 14, "normal"))

class PongBall(t.Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.shape("circle")
        self.shapesize(0.8,0.8)
        self.x_move = 10
        self.y_move = 10
        self.ballSpeed = 0.09

    def move(self):
        self.setpos(self.xcor()+self.x_move, self.ycor()+self.y_move)

    def wall_collision(self):
        
        print((self.xcor(), self.ycor()))
        gameOn = True
        if self.ycor() > 287 or self.ycor() < -290:
            self.y_move *= -1
            
        elif self.xcor() > 390 or self.xcor() < -390:
            # self.x_move *= -1
            gameOn = False

        else:
            pass

        return gameOn
    
    def pad_collision(self, pad1, pad2):

        collide = True
        if self.distance(pad2) < 50 and self.xcor() > 345:
            print("pad2")
            self.x_move *= -1
            pad2.score += 1
            # self.ballSpeed *= 0.9

        elif self.distance(pad1) < 50 and self.xcor() < -350:
            print("pad1")
            self.x_move *= -1
            pad1.score += 1
            # self.ballSpeed *= 0.9 
        
        else:
            collide = False

        return collide


    