import tkinter as tk
import turtle
import random
#이유리 22102550
class TurtleRunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=20, ai_timer_msec=100, game_timer_sec=30):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2
        self.ai_timer_msec = ai_timer_msec
        self.score = 0
        self.game_timer_sec = game_timer_sec
        self.game_over = False

        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score: {self.score}   Timer: {self.game_timer_sec} s')

        # Set up borders
        self.screen_width = canvas.window_width() // 2
        self.screen_height = canvas.window_height() // 2
        self.boundary_x = self.screen_width - 20
        self.boundary_y = self.screen_height - 20

        self.initial_runner_position = None

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def start(self, init_dist=400):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        # Store the initial position of the runner
        self.initial_runner_position = self.runner.pos()  
        
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        self.update_timer()

    def step(self):
        if not self.game_over:
            self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
            self.chaser.run_ai(self.runner.pos(), self.runner.heading())

            # Check if runner goes out of bounds and adjust its position
            runner_x, runner_y = self.runner.pos()
            if abs(runner_x) >= self.boundary_x:
                self.runner.setx(self.boundary_x if runner_x > 0 else -self.boundary_x)
            if abs(runner_y) >= self.boundary_y:
                self.runner.sety(self.boundary_y if runner_y > 0 else -self.boundary_y)

            # Check for collisions
            if self.is_catched():
                # Hide the runner when caught
                self.runner.hideturtle() 

                self.score += 1
                self.update_score()
                 # Respawn the runner when caught
                self.respawn_runner() 

            # Move the game forward
            if self.game_timer_sec > 0:
                # Update the timer here
                self.game_timer_sec -= self.ai_timer_msec / 1000  
                self.update_timer()
                self.canvas.ontimer(self.step, self.ai_timer_msec)
            else:
                self.game_over = True
                self.show_game_over_screen()

    def update_timer(self):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score: {self.score}   Timer: {self.game_timer_sec:.0f} s')

    def update_score(self):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score: {self.score}')

    def show_game_over_screen(self):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0, 0)
        self.drawer.write('Game Over', align='center', font=('Arial', 24, 'normal'))
        self.drawer.setpos(0, -50)
        self.drawer.write(f'Final Score: {self.score}', align='center', font=('Arial', 16, 'normal'))

    def respawn_runner(self):
        # Respawn the runner in a new random location inside the arena
        self.runner.showturtle()  # Make the runner visible again
        x = random.uniform(-self.boundary_x, self.boundary_x)
        y = random.uniform(-self.boundary_y, self.boundary_y)
        self.runner.setpos(x, y)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10, boundary_x=0, boundary_y=0):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y

        canvas.onkeypress(lambda: self.move_forward(), 'Up')
        canvas.onkeypress(lambda: self.move_backward(), 'Down')
        canvas.onkeypress(lambda: self.move_left(), 'Left')
        canvas.onkeypress(lambda: self.move_right(), 'Right')

        canvas.listen()

    def move_forward(self):
        new_x, new_y = self.xcor(), self.ycor() + self.step_move
        if abs(new_y) <= self.boundary_y:
            self.sety(new_y)

    def move_backward(self):
        new_x, new_y = self.xcor(), self.ycor() - self.step_move
        if abs(new_y) <= self.boundary_y:
            self.sety(new_y)

    def move_left(self):
        new_x, new_y = self.xcor() - self.step_move, self.ycor()
        if abs(new_x) <= self.boundary_x:
            self.setx(new_x)

    def move_right(self):
        new_x, new_y = self.xcor() + self.step_move, self.ycor()
        if abs(new_x) <= self.boundary_x:
            self.setx(new_x)

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=100, step_turn=100):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Turtle Runaway")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("lightgreen")

    boundary_x = canvas.winfo_width() // 2 - 20
    boundary_y = canvas.winfo_height() // 2 - 20

    runner = RandomMover(screen, step_move=40, step_turn=40)
    chaser = ManualMover(screen, boundary_x=boundary_x, boundary_y=boundary_y)

    game = TurtleRunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
