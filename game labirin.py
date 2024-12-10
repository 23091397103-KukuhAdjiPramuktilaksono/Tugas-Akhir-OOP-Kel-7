import tkinter as tk
from abc import ABC, abstractmethod

class GameObject(ABC):
    """Kelas abstrak untuk elemen permainan."""
    def __init__(self, row, col):
        self.position = [row, col]

    @abstractmethod
    def draw(self, canvas):
        pass
        
class Maze(GameObject):
    def __init__(self, structure):
        super().__init__(0, 0)  # Labirin tidak memiliki posisi spesifik
        self.structure = structure

    def draw(self, canvas):
        for row in range(len(self.structure)):
            for col in range(len(self.structure[row])):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                if self.structure[row][col] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="black")

class Player(GameObject):
    def draw(self, canvas):
        x1, y1 = self.position[1] * 50, self.position[0] * 50
        x2, y2 = x1 + 50, y1 + 50
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

    def move(self, direction, maze):
        new_position = self.position[:]
        if direction == "Up":
            new_position[0] -= 1
        elif direction == "Down":
            new_position[0] += 1
        elif direction == "Left":
            new_position[1] -= 1
        elif direction == "Right":
            new_position[1] += 1

        if maze.structure[new_position[0]][new_position[1]] == 0:
            self.position = new_position

class Goal(GameObject):
    def draw(self, canvas):
        x1, y1 = self.position[1] * 50, self.position[0] * 50
        x2, y2 = x1 + 50, y1 + 50
        canvas.create_rectangle(x1, y1, x2, y2, fill="green")

class Game:
    CELL_SIZE = 50

    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game with Multiple Levels")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text="Time: 0", font=("Arial", 16))
        self.timer_label.pack()
        self.score_label = tk.Label(self.root, text="Total Score: 0", font=("Arial", 16))
        self.score_label.pack()

        self.levels = [
            {
                "maze": [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ],
                "player": [1, 1],
                "goal": [7, 8],
            },
            {
                "maze": [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ],
                "player": [1, 1],
                "goal": [6, 8],
            },
            {
                "maze": [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                    [1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
                    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ],
                "player": [1, 1],
                "goal": [7, 7],
            },
        ]

        self.current_level = 0
        self.start_time = time.time()
        self.total_score = 0

        self.load_level()
        self.root.bind("<Key>", self.handle_input)
        self.update_timer()

    def load_level(self):
        level_data = self.levels[self.current_level]
        self.maze = Maze(level_data["maze"])
        self.player = Player(*level_data["player"])
        self.goal = Goal(*level_data["goal"])
        self.start_time = time.time()
        self.draw_elements()

    def draw_elements(self):
        self.canvas.delete("all")
        self.maze.draw(self.canvas)
        self.goal.draw(self.canvas)
        self.player.draw(self.canvas)

    def handle_input(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.player.move(event.keysym, self.maze)
            self.check_goal()
            self.draw_elements()

    def check_goal(self):
        if self.player.position == self.goal.position:
            self.finish_level()

    def finish_level(self):
        elapsed_time = int(time.time() - self.start_time)
        level_score = max(100 - elapsed_time * 10, 0)
        self.total_score += level_score
        self.score_label.config(text=f"Total Score: {self.total_score}")
        self.current_level += 1

        if self.current_level < len(self.levels):
            self.load_level()
        else:
            self.end_game()

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}")
        self.root.after(1000, self.update_timer)

    def end_game(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            250, 200, text="Game Over!", font=("Arial", 24), fill="red"
        )
        self.canvas.create_text(
            250, 250, text=f"Final Score: {self.total_score}", font=("Arial", 18), fill="blue"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

