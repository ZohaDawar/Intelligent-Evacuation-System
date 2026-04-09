"""
Graphical User Interface for Intelligent Evacuation Agent System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from agent import AutonomousEvacuationAgent, evacuation_agent
from graph import plot_algorithm_comparison

# Sample grids
SAMPLE_GRIDS = {
    "Simple Grid": [
        ['S', '.', '.', 'E'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.']
    ],
    
    "Grid with Obstacles": [
        ['S', '.', 'X', 'E'],
        ['.', 'X', '.', '.'],
        ['.', '.', '.', 'X'],
        ['.', '.', '.', '.']
    ],
    
    "Complex Maze": [
        ['S', '.', 'X', 'X', 'E'],
        ['.', 'X', '.', 'X', '.'],
        ['.', '.', '.', 'X', '.'],
        ['X', 'X', '.', '.', '.'],
        ['.', '.', '.', 'X', '.']
    ],
    
    "Fire Hazard Grid": [
        ['S', '.', 'F', '.', 'E'],
        ['.', 'X', '.', 'F', '.'],
        ['.', '.', '.', 'X', '.'],
        ['F', '.', '.', '.', 'E']
    ]
}

class EvacuationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Evacuation Agent")
        self.root.geometry("1000x700")

        self.current_grid = None
        self.start = None
        self.goal = None

        self.setup_ui()
        self.load_grid("Grid with Obstacles")

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # LEFT PANEL
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(left_panel, text="Select Grid").pack()

        self.grid_var = tk.StringVar(value="Grid with Obstacles")
        for name in SAMPLE_GRIDS:
            tk.Radiobutton(left_panel, text=name, variable=self.grid_var,
                           value=name, command=self.on_grid_select).pack(anchor="w")

        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        tk.Label(left_panel, text="Algorithm Mode").pack()

        self.algo_mode = tk.StringVar(value="Autonomous")

        tk.Radiobutton(left_panel, text="Autonomous", variable=self.algo_mode,
                       value="Autonomous").pack(anchor="w")

        tk.Radiobutton(left_panel, text="BFS", variable=self.algo_mode,
                       value="BFS").pack(anchor="w")

        tk.Radiobutton(left_panel, text="A*", variable=self.algo_mode,
                       value="A*").pack(anchor="w")

        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        tk.Button(left_panel, text="Run", command=self.run_evacuation).pack(pady=10)

        # RIGHT PANEL
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right_panel, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(right_panel, height=10)
        self.result_text.pack(fill=tk.X)

    def on_grid_select(self):
        self.load_grid(self.grid_var.get())

    def load_grid(self, name):
        self.current_grid = [row[:] for row in SAMPLE_GRIDS[name]]
        self.find_positions()
        self.draw_grid()

    def find_positions(self):
        for i in range(len(self.current_grid)):
            for j in range(len(self.current_grid[0])):
                if self.current_grid[i][j] == 'S':
                    self.start = (i, j)
                elif self.current_grid[i][j] == 'E':
                    self.goal = (i, j)

    def draw_grid(self, path=None):
        self.canvas.delete("all")

        rows = len(self.current_grid)
        cols = len(self.current_grid[0])
        size = 50

        for i in range(rows):
            for j in range(cols):
                x1, y1 = j * size, i * size
                x2, y2 = x1 + size, y1 + size

                cell = self.current_grid[i][j]

                color = "white"
                if cell == 'S': color = "green"
                elif cell == 'E': color = "blue"
                elif cell == 'X': color = "gray"
                elif cell == 'F': color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        if path:
            for (i, j) in path:
                x1, y1 = j * size, i * size
                x2, y2 = x1 + size, y1 + size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")

    def run_evacuation(self):
        try:
            mode = self.algo_mode.get()

            if mode == "Autonomous":
                agent = AutonomousEvacuationAgent(self.current_grid, self.start, self.goal)
                results = agent.run()
                path = results['result']['path']

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, results['detailed_explanation'])
                self.result_text.insert(tk.END, "\n\n" + results['comparison'])

                # GRAPH
                plot_algorithm_comparison(results['bfs_result'], results['astar_result'])

            else:
                path, explanation, nodes, time_taken, full = evacuation_agent(
                    self.current_grid, self.start, self.goal, mode
                )

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, explanation)

            self.draw_grid(path)

        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = EvacuationGUI(root)
    root.mainloop()
