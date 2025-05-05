import pongUtil as pu, time

SCREEN = pu.PongScreen()

PAD1 = pu.PongPaddle()
PAD1.setpos(-360, 0)

PAD2 = pu.PongPaddle()
PAD2.setpos(355, 0)

SCORE1 = pu.Score()
SCORE1.setpos(-200, 277)
SCORE1.refreshScore(f"P1 Score: {PAD1.score}")

SCORE2 = pu.Score()
SCORE2.setpos(200, 277)
SCORE2.refreshScore(f"P2 Score: {PAD2.score}")

ball = pu.PongBall()


SCREEN.screen.update()
SCREEN.screen.listen()
SCREEN.screen.onkeypress(PAD1.up, "w")
SCREEN.screen.onkeypress(PAD1.down, "s")
SCREEN.screen.onkeypress(PAD2.up, "Up")
SCREEN.screen.onkeypress(PAD2.down, "Down")
gameOn = True
sleepFactor = 0.1
while gameOn:
    ball.move()
    time.sleep(0.05)
    SCREEN.screen.update()
    collide = ball.pad_collision(PAD1, PAD2)
    SCORE1.refreshScore(f"P1 Score: {PAD1.score}")
    SCORE2.refreshScore(f"P2 Score: {PAD2.score}")
    if not collide:
        gameOn = ball.wall_collision()
    

gameOver = pu.Score()
if(PAD1.score >= PAD2.score):
    gameOver.refreshScore("Game Over!\nPlayer 1 wins!")

elif (PAD2.score > PAD1.score):
    gameOver.refreshScore("Game Over!\nPlayer 2 wins!")

else:
    pass


SCREEN.screen.exitonclick()