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

