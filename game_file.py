import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.geometry("400x400")
        self.master.bind("<Key>", self.handle_key)

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0

        self.init_grid()
        self.add_tile()
        self.update_grid()

    def init_grid(self):
        """Initializes the grid with empty tiles."""
        self.tiles = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(self.master, text="", font=("Helvetica", 32), width=4, height=2, relief="raised")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def add_tile(self):
        """Adds a new tile (2 or 4) to a random empty position on the grid."""
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        """Updates the graphical representation of the grid."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value == 0:
                    self.tiles[i][j].configure(text="", bg="lightgray")
                else:
                    self.tiles[i][j].configure(text=str(value), bg="lightblue")
        self.master.update_idletasks()

    def handle_key(self, event):
        """Handles key presses and moves tiles accordingly."""
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.move_tiles(event.keysym)
            self.add_tile()
            self.update_grid()
            if self.check_game_over():
                print(f"Game Over! Score: {self.score}")

    def move_tiles(self, direction):
        """Moves and merges tiles based on the direction."""
        if direction == 'Up':
            self.grid = self.transpose(self.grid)
            self.grid = self.move_left(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'Down':
            self.grid = self.reverse(self.transpose(self.grid))
            self.grid = self.move_left(self.grid)
            self.grid = self.transpose(self.reverse(self.grid))
        elif direction == 'Left':
            self.grid = self.move_left(self.grid)
        elif direction == 'Right':
            self.grid = self.reverse(self.grid)
            self.grid = self.move_left(self.grid)
            self.grid = self.reverse(self.grid)

    def move_left(self, grid):
        """Moves tiles to the left and merges them if possible."""
        new_grid = [self.merge_left(row) for row in grid]
        return new_grid

    def merge_left(self, row):
        """Merges the tiles in a row to the left."""
        new_row = [tile for tile in row if tile != 0]  # Remove zeros
        merged_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i < len(new_row) - 1 and new_row[i] == new_row[i + 1]:
                merged_row.append(new_row[i] * 2)
                self.score += new_row[i] * 2
                skip = True
            else:
                merged_row.append(new_row[i])
        # Fill the remaining space with zeros
        merged_row.extend([0] * (self.grid_size - len(merged_row)))
        return merged_row

    def check_game_over(self):
        """Checks if the game is over (no moves possible)."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    @staticmethod
    def transpose(matrix):
        """Transposes the matrix (rotates the grid)."""
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    @staticmethod
    def reverse(matrix):
        """Reverses each row of the matrix."""
        return [row[::-1] for row in matrix]

def main():
    """Main function to start the game."""
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
