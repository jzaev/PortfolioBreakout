import turtle
from time import sleep

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_Y = -250
BALL_SPEED = 0.5
PADDLE_SPEED = 20
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 30
BLOCK_SPACING = 10
ROWS = 5
COLUMNS = 8
H_COEFFICIENT = 20
FONT = ("Arial", 24, "normal")
COLORS = {0: "red", 1: "green", 2: "blue", 3: "white", 4: "orange", 5: "magenta"}
LIVES = 3


class Block(turtle.Turtle):
    def __init__(self, x, y, color="green"):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=BLOCK_HEIGHT / H_COEFFICIENT, stretch_len=BLOCK_WIDTH / H_COEFFICIENT)
        self.penup()
        self.speed(0)
        self.goto(x, y)


class Paddle(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=PADDLE_HEIGHT / H_COEFFICIENT, stretch_len=PADDLE_WIDTH / H_COEFFICIENT)
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def move_left(self):

        if self.xcor() - PADDLE_SPEED < -SCREEN_WIDTH / 2 + PADDLE_WIDTH / 2:
            self.setx(-SCREEN_WIDTH / 2 + PADDLE_WIDTH / 2)
        else:
            self.setx(self.xcor() - PADDLE_SPEED)

    def move_right(self):

        if self.xcor() + PADDLE_SPEED > SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2:
            self.setx(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2)
        else:
            self.setx(self.xcor() + PADDLE_SPEED)


class Ball:
    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.speed(1)
        self.ball.shape("circle")
        self.ball.color("red")
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = BALL_SPEED
        self.ball.dy = -BALL_SPEED
        self.ball.shapesize(stretch_wid=1, stretch_len=1)

    def move(self):
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        if self.ball.xcor() > SCREEN_WIDTH / 2 - 10 or self.ball.xcor() < -SCREEN_WIDTH / 2 + 10:
            self.ball.dx *= -1

    def bounce_x(self):
        self.ball.dx *= -1

    def bounce_y(self):
        self.ball.dy *= -1

    def reset(self):
        self.ball.goto(0, 0)


class Score(turtle.Turtle):
    def __init__(self, ball):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, SCREEN_HEIGHT / 2 - 50)
        self.update_score()
        self.ball = ball

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score}", align="center", font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_score()
        if self.score % 5 == 0:  # Increase ball speed every 5 points
            self.ball.ball.dx *= 1.1
            self.ball.ball.dy *= 1.1


class Breakout:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Breakout")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)
        self.running = True
        self.paddle = Paddle(0, -SCREEN_HEIGHT / 2 + 50)
        self.ball = Ball()
        self.lives = LIVES

        # Create blocks
        self.blocks = []
        for i in range(ROWS):
            for j in range(COLUMNS):
                x = 30 - ((COLUMNS * (BLOCK_WIDTH + BLOCK_SPACING)) / 2) + (
                        j * (BLOCK_WIDTH + BLOCK_SPACING)) + BLOCK_SPACING / 2
                y = SCREEN_HEIGHT / 2 - 100 - (i * (BLOCK_HEIGHT + BLOCK_SPACING))
                block = Block(x, y, COLORS[i])
                self.blocks.append(block)

        self.screen.listen()
        self.screen.onkey(self.paddle.move_left, "Left")
        self.screen.onkey(self.paddle.move_right, "Right")
        self.screen.onkey(self.stop, "q")  # Added key to exit the game
        self.score = Score(self.ball)  # Add score display

        self.screen.cv.bind('<Motion>', self.on_mouse_move)  # Register the on_mouse_move function for mouse control

    def on_mouse_move(self, event):
        x = event.x - SCREEN_WIDTH // 2
        self.paddle.setx(x)

    def stop(self):
        self.running = False

    def play(self):
        while self.running:
            self.screen.update()

            self.ball.move()

            if self.ball.ball.xcor() > SCREEN_WIDTH / 2 - H_COEFFICIENT \
                    or self.ball.ball.xcor() < -SCREEN_WIDTH / 2 + H_COEFFICIENT:
                self.ball.bounce_x()

            if self.ball.ball.ycor() > SCREEN_HEIGHT / 2:
                self.ball.bounce_x()

            if self.ball.ball.ycor() < -SCREEN_HEIGHT / 2:
                self.lives -= 1  # Decrease lives when the ball falls
                self.ball.reset()

            if (self.ball.ball.ycor() - H_COEFFICIENT / 2 < self.paddle.ycor() + PADDLE_HEIGHT / 2 and
                    self.ball.ball.xcor() + H_COEFFICIENT / 2 > self.paddle.xcor() - PADDLE_WIDTH / 2 and
                    self.ball.ball.xcor() - H_COEFFICIENT / 2 < self.paddle.xcor() + PADDLE_WIDTH / 2):
                self.ball.bounce_y()

            for block in self.blocks:
                if (abs(self.ball.ball.xcor() - block.xcor()) < (BLOCK_WIDTH / 2 + H_COEFFICIENT) and
                        abs(self.ball.ball.ycor() - block.ycor()) < (BLOCK_HEIGHT / 2 + H_COEFFICIENT)):
                    self.ball.bounce_y()
                    block.goto(1000, 1000)  # Move the block off-screen
                    self.blocks.remove(block)  # Remove the block from the list
                    self.score.increase_score()  # Increase the score
            if self.lives <= 0 or len(self.blocks) == 0:
                self.running = False

    def game_over(self):
        self.score.goto(0, 0)
        if self.lives == 0:
            self.score.write("Game Over", align="center", font=FONT)
        else:
            self.score.write("You Won!", align="center", font=FONT)



if __name__ == "__main__":
    game = Breakout()
    game.play()
    game.game_over()
    turtle.mainloop()