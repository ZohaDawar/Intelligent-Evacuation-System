def get_grid_info(grid):
    rows = len(grid)
    cols = len(grid[0])

    obstacles = []
    fires = []
    goals = []

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'X':
                obstacles.append((i, j))
            elif grid[i][j] == 'F':
                fires.append((i, j))
            elif grid[i][j] == 'E':
                goals.append((i, j))

    total_cells = rows * cols
    obstacle_percentage = (len(obstacles) / total_cells) * 100

    return {
        'rows': rows,
        'cols': cols,
        'total_cells': total_cells,
        'obstacles': obstacles,
        'fires': fires,
        'goals': goals,
        'obstacle_percentage': obstacle_percentage
    }


def get_grid_complexity(grid):
    info = get_grid_info(grid)
    
    if info['obstacle_percentage'] < 20:
        return "Simple"
    elif info['obstacle_percentage'] < 40:
        return "Moderate"
    else:
        return "Complex"


def estimate_path_complexity(grid, start, goal):
    distance = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    complexity = get_grid_complexity(grid)
    
    if complexity == "Simple":
        return "Easy"
    elif complexity == "Moderate":
        return "Medium"
    else:
        return "Hard"


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
