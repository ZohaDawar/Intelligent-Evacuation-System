"""
Autonomous Evacuation Agent
Decides which algorithm to use based on grid characteristics
"""

from bfs import bfs_with_analysis
from astar import astar_with_analysis
from minimax import evaluate_safety_with_alpha_beta
from utils import get_grid_info, get_grid_complexity, estimate_path_complexity
from analysis import compare_algorithms, generate_detailed_explanation

class AutonomousEvacuationAgent:
    """
    Intelligent autonomous agent that:
    1. Analyzes the environment
    2. Decides which algorithm to use
    3. Executes pathfinding
    4. Provides detailed analysis and recommendations
    """
    
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.grid_info = get_grid_info(grid)
        self.selected_algorithm = None
        self.selection_reason = None
        self.result = None
        self.safety_score = None
        self.safety_message = None
        self.comparison_result = None
        self.winner = None
    
    def analyze_environment(self):
        """
        Analyze the grid environment to make autonomous decision
        """
        complexity = get_grid_complexity(self.grid)
        path_complexity = estimate_path_complexity(self.grid, self.start, self.goal)
        distance = abs(self.start[0] - self.goal[0]) + abs(self.start[1] - self.goal[1])
        obstacle_count = len(self.grid_info['obstacles'])
        total_cells = self.grid_info['total_cells']
        
        analysis = {
            'complexity': complexity,
            'path_complexity': path_complexity,
            'distance': distance,
            'obstacle_percentage': (obstacle_count / total_cells) * 100,
            'has_fires': len(self.grid_info['fires']) > 0
        }
        
        # Autonomous decision logic
        if analysis['obstacle_percentage'] > 40:
            # Many obstacles - A* heuristic will help guide through them
            self.selected_algorithm = "A*"
            self.selection_reason = f"High obstacle density ({analysis['obstacle_percentage']:.1f}%) - A* heuristic will efficiently navigate through obstacles"
        elif analysis['distance'] > 15:
            # Long distance - A* will focus search toward goal
            self.selected_algorithm = "A*"
            self.selection_reason = f"Long evacuation distance ({analysis['distance']} steps) - A* will prioritize nodes closer to the exit"
        elif analysis['complexity'] == "Simple" and analysis['distance'] < 8:
            # Simple grid - BFS is sufficient and simpler
            self.selected_algorithm = "BFS"
            self.selection_reason = f"Simple grid with low complexity - BFS provides guaranteed shortest path with less overhead"
        elif analysis['has_fires']:
            # Fire hazards - A* is faster for quick evacuation
            self.selected_algorithm = "A*"
            self.selection_reason = "Fire hazards detected - A* finds faster evacuation routes"
        else:
            # Default to A* for better performance
            self.selected_algorithm = "A*"
            self.selection_reason = "Default optimal choice - A* balances optimality and efficiency"
        
        return analysis
    
    def run(self):
        """
        Execute the autonomous agent decision and run the selected algorithm
        """
        # Step 1: Analyze environment
        env_analysis = self.analyze_environment()
        
        # Step 2: Run safety evaluation using Alpha-Beta pruning
        self.safety_score, self.safety_message = evaluate_safety_with_alpha_beta(
            self.start, self.grid, depth=3
        )
        
        # Step 3: Run both algorithms for comparison (agent runs both internally)
        bfs_result = bfs_with_analysis(self.grid, self.start, self.goal)
        astar_result = astar_with_analysis(self.grid, self.start, self.goal)
        
        # Step 4: Generate comparison
        self.comparison_result, self.winner = compare_algorithms(bfs_result, astar_result)
        
        # Step 5: Use the selected algorithm for the main result
        if self.selected_algorithm == "BFS":
            self.result = bfs_result
        else:
            self.result = astar_result
        
        # Step 6: Generate detailed explanation
        self.detailed_explanation = generate_detailed_explanation(
            self.selected_algorithm,
            self.result,
            self.grid_info,
            self.safety_score,
            self.safety_message
        )
        
        return {
            'selected_algorithm': self.selected_algorithm,
            'selection_reason': self.selection_reason,
            'result': self.result,
            'safety_score': self.safety_score,
            'safety_message': self.safety_message,
            'comparison': self.comparison_result,
            'winner': self.winner,
            'detailed_explanation': self.detailed_explanation,
            'env_analysis': env_analysis
        }
    
    def get_path(self):
        """Return the computed path"""
        return self.result.get('path', None) if self.result else None
    
    def get_nodes_explored(self):
        """Return number of nodes explored"""
        return self.result.get('nodes_explored', 0) if self.result else 0
    
    def get_time_taken(self):
        """Return time taken for execution"""
        return self.result.get('time_taken', 0) if self.result else 0


# Legacy function for backward compatibility
def evacuation_agent(grid, start, goal, algorithm=None):
    """
    Legacy evacuation agent function
    
    If algorithm is specified, uses that algorithm.
    If algorithm is None, agent autonomously decides.
    """
    agent = AutonomousEvacuationAgent(grid, start, goal)
    
    if algorithm and algorithm in ["BFS", "A*"]:
        # Override agent's decision
        agent.selected_algorithm = algorithm
        agent.selection_reason = f"User manually selected {algorithm}"
    
    results = agent.run()
    
    path = results['result'].get('path')
    explanation = results['detailed_explanation']
    nodes = results['result'].get('nodes_explored', 0)
    time_taken = results['result'].get('time_taken', 0)
    
    return path, explanation, nodes, time_taken, results
