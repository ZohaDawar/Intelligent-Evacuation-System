"""
Breadth-First Search (BFS) Implementation
Explores all directions equally - guarantees shortest path in unweighted grid
"""

from collections import deque

def bfs(grid, start, goal):
    """
    BFS algorithm for pathfinding
    
    Args:
        grid: 2D list representing the map
        start: tuple (x, y) starting position
        goal: tuple (x, y) goal position
    
    Returns:
        path: list of coordinates from start to goal
        nodes_explored: number of nodes visited
        max_queue_size: maximum size of the queue during search
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = set([start])
    nodes_explored = 1
    max_queue_size = 1
    
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        (x, y), path = queue.popleft()
        
        if (x, y) == goal:
            return path, nodes_explored, max_queue_size
        
        # Explore all 4 directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != 'X' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    nodes_explored += 1
                    queue.append(((nx, ny), path + [(nx, ny)]))
    
    return None, nodes_explored, max_queue_size

def bfs_with_analysis(grid, start, goal):
    """BFS with additional analysis metrics"""
    import time
    
    start_time = time.time()
    path, nodes_explored, max_queue = bfs(grid, start, goal)
    end_time = time.time()
    
    return {
        'algorithm': 'BFS',
        'path': path,
        'path_length': len(path) if path else float('inf'),
        'nodes_explored': nodes_explored,
        'time_taken': end_time - start_time,
        'max_queue_size': max_queue,
        'success': path is not None
    }
