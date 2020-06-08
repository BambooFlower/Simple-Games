# Simple Pong game using Turtle

import turtle 
import os

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)


# Score
scoreA = 0
scoreB = 0


# Paddle A
paddleA = turtle.Turtle()
paddleA.speed(0) # Animation speed
paddleA.shape("square")
paddleA.color("white")
paddleA.shapesize(stretch_wid=5, stretch_len=1)
paddleA.penup() # To don't draw a line when it updates 
paddleA.goto(-350,0) # Starting coordinate
 

# Paddle B
paddleB = turtle.Turtle()
paddleB.speed(0) 
paddleB.shape("square")
paddleB.color("white")
paddleB.shapesize(stretch_wid=5, stretch_len=1)
paddleB.penup() 
paddleB.goto(350,0) 


# Ball
ball = turtle.Turtle()
ball.speed(0) 
ball.shape("square")
ball.color("white")
ball.penup() 
ball.goto(0,0) 
ball.dx = 0.1 # ball speed in the x-axis
ball.dy = 0.1 # ball speed in the y-axis


# Scoring Count
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle() # To hide the pen, we just want to see the score
pen.goto(0,260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))


# Paddle movement 
# Paddle A
def paddleA_up():
	y = paddleA.ycor()
	y += 25
	paddleA.sety(y)

def paddleA_down():
	y = paddleA.ycor()
	y -= 25
	paddleA.sety(y)


# Paddle B
def paddleB_up():
	y = paddleB.ycor()
	y += 25
	paddleB.sety(y)

def paddleB_down():
	y = paddleB.ycor()
	y -= 25
	paddleB.sety(y)


# Keyboard Binding 
wn.listen()
wn.onkey(paddleA_up, "w")
wn.onkey(paddleA_down, "s")
wn.onkey(paddleB_up, "Up")
wn.onkey(paddleB_down, "Down")


# Main game loop
while True:
	wn.update()

	# Move the ball
	ball.setx(ball.xcor() + ball.dx)
	ball.sety(ball.ycor() + ball.dy)

	# Border Checking 
	# Ball Top & Bottom
	if ball.ycor() > 290:
		ball.sety(290)
		ball.dy *= -1  # Reverse the direction
		# Linux Implementation
		os.system("aplay bounce.wav&") # Sound
		# MacOS Implementation
		# os.system("afplay bound.wav&")
		# Windows Implementation
		# Google it ...

	if ball.ycor() < -290:
		ball.sety(-290)
		ball.dy *= -1  # Reverse the direction
		os.system("aplay bounce.wav&")

	# Paddle A Top & Bottom
	if paddleA.ycor() > 220:
		paddleA.sety(220)

	if paddleA.ycor() < -220:
		paddleA.sety(-220)

	# Paddle B Top & Bottom
	if paddleB.ycor() > 220:
		paddleB.sety(220)

	if paddleB.ycor() < -220:
		paddleB.sety(-220)

	# Left & Right 
	if ball.xcor() > 390:
		ball.goto(0,0)
		ball.dx *= -1
		scoreA += 1
		# Score Update
		pen.clear()
		pen.write("Player A: {}  Player B: {}".format(scoreA, scoreB), align="center", font=("Courier", 24, "normal"))

	if ball.xcor() < -390:
		ball.goto(0,0)
		ball.dx *= -1
		scoreB += 1
		# Score Update
		pen.clear()
		pen.write("Player A: {}  Player B: {}".format(scoreA, scoreB), align="center", font=("Courier", 24, "normal"))

	# Paddle-Ball Collision
	if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddleA.ycor() + 40 and ball.ycor() > paddleA.ycor() - 40):
		ball.setx(-340)
		ball.dx *= -1
		os.system("aplay bounce.wav&")

	if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddleB.ycor() + 40 and ball.ycor() > paddleB.ycor() - 40):
		ball.setx(340)
		ball.dx *= -1
		os.system("aplay bounce.wav&")
