import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.direction = 'Right'
        self.running = True
        self.score = 0
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = None
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.root.bind('<Up>', self.go_up)
        self.root.bind('<Down>', self.go_down)
        self.root.bind('<Left>', self.go_left)
        self.root.bind('<Right>', self.go_right)
        self.place_food()
        self.update()

    def place_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def go_up(self, event):
        if self.direction != 'Down':
            self.direction = 'Up'

    def go_down(self, event):
        if self.direction != 'Up':
            self.direction = 'Down'

    def go_left(self, event):
        if self.direction != 'Right':
            self.direction = 'Left'

    def go_right(self, event):
        if self.direction != 'Left':
            self.direction = 'Right'

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)
        self.snake = [new_head] + self.snake[:-1]

    def grow_snake(self):
        self.snake.append(self.snake[-1])

    def check_collision(self):
        head_x, head_y = self.snake[0]
        # Wall collision
        if not (0 <= head_x < self.width // self.cell_size and 0 <= head_y < self.height // self.cell_size):
            return True
        # Self collision
        if (head_x, head_y) in self.snake[1:]:
            return True
        return False

    def update(self):
        if not self.running:
            return
        self.move_snake()
        if self.snake[0] == self.food:
            self.grow_snake()
            self.score += 1
            self.place_food()
        if self.check_collision():
            self.running = False
            self.canvas.create_text(self.width//2, self.height//2, fill="red", font=("Arial", 24), text="Game Over")
            return
        self.draw()
        self.root.after(100, self.update)

    def draw(self):
        self.canvas.delete("all")
        # Draw food
        x, y = self.food
        self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                     (x+1)*self.cell_size, (y+1)*self.cell_size,
                                     fill="red", outline="")
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = "green" if i == 0 else "#00cc00"
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                         (x+1)*self.cell_size, (y+1)*self.cell_size,
                                         fill=color, outline="")
        # Draw score
        self.canvas.create_text(40, 10, fill="white", font=("Arial", 12), text=f"Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
