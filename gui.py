"""
Graphical User Interface for Intelligent Evacuation Agent System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from agent import AutonomousEvacuationAgent, evacuation_agent

# Sample grids for demonstration
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
    ],
    
    "Large Grid": [
        ['S', '.', '.', '.', '.', '.', 'E'],
        ['.', 'X', 'X', '.', 'X', '.', '.'],
        ['.', '.', 'X', '.', '.', '.', 'X'],
        ['.', 'X', '.', '.', 'X', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', 'X', '.', '.', '.', 'X', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]
}

class EvacuationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏃 Intelligent Evacuation Agent System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.current_grid = None
        self.start = None
        self.goal = None
        
        self.setup_ui()
        self.load_grid("Grid with Obstacles")
    
    def setup_ui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(title_frame, text="🤖 Intelligent Evacuation Agent System",
                               font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, 
                                  text="Autonomous Pathfinding | BFS vs A* | Minimax + Alpha-Beta Safety Analysis",
                                  font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Grid selection
        grid_label = tk.Label(left_panel, text="🗺️ SELECT GRID", 
                              font=('Arial', 12, 'bold'), fg='white', bg='#34495e')
        grid_label.pack(pady=(10, 5))
        
        self.grid_var = tk.StringVar(value="Grid with Obstacles")
        for grid_name in SAMPLE_GRIDS.keys():
            rb = tk.Radiobutton(left_panel, text=grid_name, variable=self.grid_var,
                               value=grid_name, command=self.on_grid_select,
                               fg='white', bg='#34495e', selectcolor='#2c3e50')
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        tk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Algorithm selection (User can override agent decision)
        algo_label = tk.Label(left_panel, text="⚙️ ALGORITHM MODE", 
                              font=('Arial', 12, 'bold'), fg='white', bg='#34495e')
        algo_label.pack(pady=(10, 5))
        
        self.algo_mode = tk.StringVar(value="Autonomous")
        
        auto_rb = tk.Radiobutton(left_panel, text="🤖 Autonomous (Agent Decides)", 
                                variable=self.algo_mode, value="Autonomous",
                                fg='white', bg='#34495e', selectcolor='#2c3e50')
        auto_rb.pack(anchor=tk.W, padx=20, pady=2)
        
        bfs_rb = tk.Radiobutton(left_panel, text="📊 BFS Only", 
                               variable=self.algo_mode, value="BFS",
                               fg='white', bg='#34495e', selectcolor='#2c3e50')
        bfs_rb.pack(anchor=tk.W, padx=20, pady=2)
        
        astar_rb = tk.Radiobutton(left_panel, text="⭐ A* Only", 
                                 variable=self.algo_mode, value="A*",
                                 fg='white', bg='#34495e', selectcolor='#2c3e50')
        astar_rb.pack(anchor=tk.W, padx=20, pady=2)
        
        tk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Run button
        self.run_button = tk.Button(left_panel, text="🚀 RUN EVACUATION", 
                                    command=self.run_evacuation,
                                    font=('Arial', 14, 'bold'), bg='#e74c3c', 
                                    fg='white', padx=20, pady=10)
        self.run_button.pack(pady=20)
        
        # Status
        self.status_label = tk.Label(left_panel, text="Ready", 
                                     font=('Arial', 10), fg='#2ecc71', bg='#34495e')
        self.status_label.pack(pady=10)
        
        # Right panel - Grid Display
        right_panel = tk.Frame(main_frame, bg='#2c3e50')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Grid canvas
        self.grid_canvas = tk.Canvas(right_panel, bg='white', highlightthickness=2, 
                                     highlightbackground='#3498db')
        self.grid_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Results frame
        results_frame = tk.Frame(right_panel, bg='#34495e', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results text with scrollbar
        text_frame = tk.Frame(results_frame, bg='#34495e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 9),
                                    bg='#2c3e50', fg='#ecf0f1', insertbackground='white')
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def on_grid_select(self):
        """Handle grid selection"""
        self.load_grid(self.grid_var.get())
    
    def load_grid(self, grid_name):
        """Load a sample grid"""
        self.current_grid = [row[:] for row in SAMPLE_GRIDS[grid_name]]
        self.find_start_and_goal()
        self.draw_grid()
        self.status_label.config(text=f"Loaded: {grid_name}", fg='#2ecc71')
    
    def find_start_and_goal(self):
        """Find start (S) and goal (E) positions"""
        for i in range(len(self.current_grid)):
            for j in range(len(self.current_grid[0])):
                if self.current_grid[i][j] == 'S':
                    self.start = (i, j)
                elif self.current_grid[i][j] == 'E':
                    self.goal = (i, j)
    
    def draw_grid(self, path=None):
        """Draw the grid on canvas"""
        if self.current_grid is None:
            return
        
        self.grid_canvas.delete("all")
        
        rows = len(self.current_grid)
        cols = len(self.current_grid[0])
        
        # Calculate cell size
        canvas_width = self.grid_canvas.winfo_width()
        canvas_height = self.grid_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 400
        
        cell_size = min(canvas_width // cols, canvas_height // rows)
        
        # Calculate offset to center the grid
        offset_x = (canvas_width - cell_size * cols) // 2
        offset_y = (canvas_height - cell_size * rows) // 2
        
        # Draw grid cells
        for i in range(rows):
            for j in range(cols):
                x1 = offset_x + j * cell_size
                y1 = offset_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                cell = self.current_grid[i][j]
                
                # Set color based on cell type
                if cell == 'S':
                    color = '#2ecc71'  # Green - Start
                elif cell == 'E':
                    color = '#3498db'  # Blue - Exit
                elif cell == 'F':
                    color = '#e74c3c'  # Red - Fire
                elif cell == 'X':
                    color = '#7f8c8d'  # Gray - Obstacle
                else:
                    color = '#ecf0f1'  # Light gray - Path
                
                self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#bdc3c7')
                
                # Add text for special cells
                if cell == 'S':
                    self.grid_canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="S", 
                                                 font=('Arial', cell_size//3, 'bold'), fill='white')
                elif cell == 'E':
                    self.grid_canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="E", 
                                                 font=('Arial', cell_size//3, 'bold'), fill='white')
                elif cell == 'F':
                    self.grid_canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="🔥", 
                                                 font=('Arial', cell_size//3), fill='white')
                elif cell == 'X':
                    self.grid_canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="█", 
                                                 font=('Arial', cell_size//3), fill='white')
        
        # Draw path if provided
        if path:
            for idx, (i, j) in enumerate(path):
                if self.current_grid[i][j] not in ['S', 'E']:
                    x1 = offset_x + j * cell_size
                    y1 = offset_y + i * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    
                    # Highlight path with yellow
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill='#f1c40f', outline='#bdc3c7')
                    
                    # Add step number for small paths
                    if len(path) < 20:
                        self.grid_canvas.create_text((x1 + x2)//2, (y1 + y2)//2, 
                                                     text=str(idx), font=('Arial', cell_size//4), 
                                                     fill='#2c3e50')
    
    def run_evacuation(self):
        """Run the evacuation agent"""
        if self.current_grid is None:
            messagebox.showerror("Error", "No grid loaded!")
            return
        
        # Update status
        self.status_label.config(text="Running evacuation...", fg='#f39c12')
        self.run_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Determine algorithm mode
            algo_mode = self.algo_mode.get()
            
            if algo_mode == "Autonomous":
                # Let agent decide
                agent = AutonomousEvacuationAgent(self.current_grid, self.start, self.goal)
                results = agent.run()
                path = results['result'].get('path')
                explanation = results['detailed_explanation']
                nodes = results['result'].get('nodes_explored', 0)
                time_taken = results['result'].get('time_taken', 0)
                
                # Also show comparison
                comparison = results['comparison']
                full_output = f"{explanation}\n\n{comparison}"
                
            else:
                # Use specified algorithm
                algorithm = algo_mode
                path, explanation, nodes, time_taken, full_results = evacuation_agent(
                    self.current_grid, self.start, self.goal, algorithm
                )
                full_output = explanation
                
                # Add comparison if available
                if 'comparison' in full_results:
                    full_output += f"\n\n{full_results['comparison']}"
            
            # Draw path on grid
            self.draw_grid(path)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, full_output)
            self.results_text.see(tk.END)
            
            # Update status
            if path:
                self.status_label.config(text=f"✅ Evacuation complete! Path found in {time_taken:.4f}s", 
                                        fg='#2ecc71')
            else:
                self.status_label.config(text="❌ No path found!", fg='#e74c3c')
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_label.config(text="Error occurred", fg='#e74c3c')
        
        finally:
            self.run_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = EvacuationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
