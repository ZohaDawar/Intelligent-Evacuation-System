"""
Minimax Algorithm with Alpha-Beta Pruning
Used for safety evaluation and risk assessment
"""

def evaluate_position(position, grid):
    """
    Evaluate the safety score of a position
    
    Scores:
    -100: Fire position (dangerous)
    -50: Adjacent to fire
    0: Neutral position
    10: Safe position (empty or path)
    50: Exit/Goal position
    """
    x, y = position
    rows, cols = len(grid), len(grid[0])
    
    # Check current cell
    if grid[x][y] == 'F':
        return -100
    elif grid[x][y] == 'E':
        return 50
    elif grid[x][y] == 'X':
        return -float('inf')
    
    # Check adjacent cells for fire proximity penalty
    fire_adjacent = False
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == 'F':
                fire_adjacent = True
                break
    
    if fire_adjacent:
        return -50
    
    return 10

def get_valid_moves(position, grid):
    """Get all valid moves from current position"""
    x, y = position
    rows, cols = len(grid), len(grid[0])
    moves = []
    
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] != 'X':
                moves.append((nx, ny))
    
    return moves

def minimax(position, grid, depth, is_maximizing):
    """
    Minimax algorithm for safety evaluation
    
    Args:
        position: current position tuple (x, y)
        grid: game grid
        depth: search depth
        is_maximizing: True for agent's turn, False for environment/fire
    
    Returns:
        best score for the position
    """
    if depth == 0:
        return evaluate_position(position, grid)
    
    if is_maximizing:
        best_score = -float('inf')
        for move in get_valid_moves(position, grid):
            score = minimax(move, grid, depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_valid_moves(position, grid):
            score = minimax(move, grid, depth - 1, True)
            best_score = min(best_score, score)
        return best_score

def alpha_beta(position, grid, depth, alpha, beta, is_maximizing):
    """
    Alpha-Beta Pruning implementation for optimized minimax
    
    Args:
        position: current position tuple (x, y)
        grid: game grid
        depth: search depth
        alpha: best value for maximizer
        beta: best value for minimizer
        is_maximizing: True for agent's turn, False for environment
    
    Returns:
        best score with pruning optimization
    """
    if depth == 0:
        return evaluate_position(position, grid)
    
    if is_maximizing:
        best_score = -float('inf')
        for move in get_valid_moves(position, grid):
            score = alpha_beta(move, grid, depth - 1, alpha, beta, False)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cut-off
        return best_score
    else:
        best_score = float('inf')
        for move in get_valid_moves(position, grid):
            score = alpha_beta(move, grid, depth - 1, alpha, beta, True)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return best_score

def evaluate_safety_with_alpha_beta(start, grid, depth=3):
    """Convenience function to evaluate safety using Alpha-Beta"""
    score = alpha_beta(start, grid, depth, -float('inf'), float('inf'), True)
    
    # Interpret the score
    if score <= -100:
        return score, "CRITICAL: Position is extremely dangerous (fire location)"
    elif score <= -50:
        return score, "WARNING: Position is dangerous (adjacent to fire)"
    elif score <= 0:
        return score, "CAUTION: Position has moderate risk"
    elif score <= 30:
        return score, "SAFE: Position is relatively safe"
    else:
        return score, "VERY SAFE: Position is excellent (near exit)"
