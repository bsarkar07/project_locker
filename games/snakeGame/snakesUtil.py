import turtle as t, random

# Snake seg turtle
class Snakes(t.Turtle):
    
    def __init__(self, count):
        super().__init__()
        self.order = count
        self.penup()
        self.color("blue")
        self.shape("square")

    def __str__(self):
        return "Seg"+str(self.order)

# Food turtle     
class Food(t.Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.speed("fastest")
        self.color("white")
        self.shape("circle")
        self.shapesize(0.5,0.5)
    
    def rand_pos(self):
        randX = random.randint(-280, 280)
        randY = random.randint(-280, 280)
        self.setpos(randX,randY)

# Score Turtle
class Score(t.Turtle):
    
    def __init__(self, score):
        super().__init__()
        self.penup()
        self.color("white")
        self.setpos(0,265)
        self.hideturtle()
        self.refreshScore(score)
        
    def refreshScore(self, score, text = "Score"):
        self.clear()
        self.write(f"{text}: {score}", align = "center", font = ("Arial", 24, "normal"))