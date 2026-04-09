"""
A* Search Algorithm Implementation
Uses Manhattan distance heuristic for efficient pathfinding
"""

import heapq

def heuristic(a, b):
    """Manhattan distance heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """
    A* algorithm for pathfinding with heuristic guidance
    
    Args:
        grid: 2D list representing the map
        start: tuple (x, y) starting position
        goal: tuple (x, y) goal position
    
    Returns:
        path: list of coordinates from start to goal
        nodes_explored: number of nodes visited
        max_heap_size: maximum size of the priority queue
    """
    rows, cols = len(grid), len(grid[0])
    
    # Priority queue: (f_score, position, path)
    # f_score = g_score + heuristic
    pq = [(heuristic(start, goal), 0, start, [start])]
    visited = set([start])
    nodes_explored = 1
    max_heap_size = 1
    
    # g_score dictionary for cost tracking
    g_score = {start: 0}
    
    while pq:
        max_heap_size = max(max_heap_size, len(pq))
        f, g, (x, y), path = heapq.heappop(pq)
        
        if (x, y) == goal:
            return path, nodes_explored, max_heap_size
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != 'X':
                    new_g = g + 1
                    
                    if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = new_g
                        new_f = new_g + heuristic((nx, ny), goal)
                        
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            nodes_explored += 1
                        
                        heapq.heappush(pq, (new_f, new_g, (nx, ny), path + [(nx, ny)]))
    
    return None, nodes_explored, max_heap_size

def astar_with_analysis(grid, start, goal):
    """A* with additional analysis metrics"""
    import time
    
    start_time = time.time()
    path, nodes_explored, max_heap = astar(grid, start, goal)
    end_time = time.time()
    
    return {
        'algorithm': 'A*',
        'path': path,
        'path_length': len(path) if path else float('inf'),
        'nodes_explored': nodes_explored,
        'time_taken': end_time - start_time,
        'max_queue_size': max_heap,
        'success': path is not None
    }
