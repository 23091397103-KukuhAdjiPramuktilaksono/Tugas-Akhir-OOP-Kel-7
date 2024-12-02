import tkinter as tk

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Labirin OOP")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        # Inisialisasi elemen game
        self.maze = Maze()
        self.player = Player(1, 1)
        self.goal = Goal(7, 8)

        # Menggambar elemen awal
        self.maze.draw(self.canvas)
        self.goal.draw(self.canvas)
        self.player.draw(self.canvas)

        # Bind input
        self.root.bind("<Key>", self.handle_input)

    def handle_input(self, event):
        direction = event.keysym
        self.player.move(direction, self.maze)
        self.canvas.delete("all")
        self.maze.draw(self.canvas)
        self.goal.draw(self.canvas)
        self.player.draw(self.canvas)

        if self.player.position == self.goal.position:
            self.canvas.create_text(250, 250, text="You Win!", font=("Arial", 24), fill="red")

    def start(self):
        self.root.mainloop()


