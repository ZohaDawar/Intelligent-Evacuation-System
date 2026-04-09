"""
Comparative Analysis Module
Compares different algorithms and generates detailed explanations
"""

from utils import get_grid_info, manhattan_distance

def compare_algorithms(bfs_result, astar_result):
    """
    Perform comparative analysis between BFS and A* algorithms
    
    Args:
        bfs_result: dictionary with BFS results
        astar_result: dictionary with A* results
    
    Returns:
        comparative_analysis: string with detailed comparison
        winner: which algorithm performed better
    """
    analysis = []
    analysis.append("=" * 60)
    analysis.append("📊 COMPARATIVE ALGORITHM ANALYSIS")
    analysis.append("=" * 60)
    
    # Check if both algorithms succeeded
    bfs_success = bfs_result.get('success', False)
    astar_success = astar_result.get('success', False)
    
    if not bfs_success and not astar_success:
        analysis.append("\n❌ Both algorithms failed to find a path!")
        analysis.append("   The goal may be unreachable due to obstacles.")
        return "\n".join(analysis), "No Winner"
    elif not bfs_success:
        analysis.append("\n❌ BFS failed to find a path, but A* succeeded!")
        return "\n".join(analysis), "A*"
    elif not astar_success:
        analysis.append("\n❌ A* failed to find a path, but BFS succeeded!")
        return "\n".join(analysis), "BFS"
    
    # Both succeeded - detailed comparison
    bfs_len = bfs_result['path_length']
    astar_len = astar_result['path_length']
    bfs_nodes = bfs_result['nodes_explored']
    astar_nodes = astar_result['nodes_explored']
    bfs_time = bfs_result['time_taken']
    astar_time = astar_result['time_taken']
    
    analysis.append("\n📈 PERFORMANCE METRICS COMPARISON")
    analysis.append("-" * 40)
    analysis.append(f"{'Metric':<20} {'BFS':<15} {'A*':<15}")
    analysis.append("-" * 40)
    analysis.append(f"{'Path Length':<20} {bfs_len:<15} {astar_len:<15}")
    analysis.append(f"{'Nodes Explored':<20} {bfs_nodes:<15} {astar_nodes:<15}")
    analysis.append(f"{'Time (seconds)':<20} {bfs_time:.5f}{'':<9} {astar_time:.5f}")
    analysis.append("-" * 40)
    
    # Path length comparison
    analysis.append("\n🎯 PATH LENGTH ANALYSIS")
    if bfs_len == astar_len:
        analysis.append("   ✅ Both algorithms found the optimal path length.")
    elif bfs_len < astar_len:
        analysis.append(f"   ✅ BFS found a SHORTER path ({bfs_len} vs {astar_len} steps)")
        analysis.append("   → BFS guarantees shortest path in unweighted grids")
    else:
        analysis.append(f"   ✅ A* found a SHORTER path ({astar_len} vs {bfs_len} steps)")
        analysis.append("   → A* with heuristic can find optimal paths")
    
    # Efficiency comparison
    analysis.append("\n⚡ EFFICIENCY ANALYSIS")
    efficiency_ratio = (astar_nodes / bfs_nodes) * 100 if bfs_nodes > 0 else 100
    
    if astar_nodes < bfs_nodes:
        reduction = bfs_nodes - astar_nodes
        percent_reduction = (reduction / bfs_nodes) * 100
        analysis.append(f"   ✅ A* was MORE EFFICIENT: explored {percent_reduction:.1f}% fewer nodes")
        analysis.append(f"   → A*'s heuristic guided search towards the goal")
        analysis.append(f"   → Saved {reduction} node expansions")
    elif astar_nodes > bfs_nodes:
        analysis.append(f"   ⚠️ BFS was MORE EFFICIENT: explored {astar_nodes - bfs_nodes} fewer nodes")
        analysis.append(f"   → For simple grids, BFS overhead is lower")
    else:
        analysis.append("   → Both algorithms explored the same number of nodes")
    
    # Speed comparison
    analysis.append("\n⏱️ SPEED ANALYSIS")
    if astar_time < bfs_time:
        speedup = (bfs_time / astar_time) if astar_time > 0 else 1
        analysis.append(f"   ✅ A* was FASTER: {speedup:.1f}x speedup over BFS")
        analysis.append(f"   → Time saved: {(bfs_time - astar_time)*1000:.2f} ms")
    elif bfs_time < astar_time:
        analysis.append(f"   ✅ BFS was FASTER: {(astar_time/bfs_time):.1f}x speedup over A*")
    else:
        analysis.append("   → Both algorithms had similar execution time")
    
    # Winner determination
    analysis.append("\n🏆 OVERALL VERDICT")
    
    # Score-based winner determination
    scores = {'BFS': 0, 'A*': 0}
    
    if bfs_len <= astar_len:
        scores['BFS'] += 1
    else:
        scores['A*'] += 1
    
    if bfs_nodes <= astar_nodes:
        scores['BFS'] += 1
    else:
        scores['A*'] += 1
    
    if bfs_time <= astar_time:
        scores['BFS'] += 1
    else:
        scores['A*'] += 1
    
    if scores['BFS'] > scores['A*']:
        winner = "BFS"
        analysis.append(f"   🥇 WINNER: BFS (Won {scores['BFS']}/3 categories)")
        analysis.append("   → Best for: Simple grids, guaranteed shortest path")
    elif scores['A*'] > scores['BFS']:
        winner = "A*"
        analysis.append(f"   🥇 WINNER: A* (Won {scores['A*']}/3 categories)")
        analysis.append("   → Best for: Complex grids with obstacles")
    else:
        winner = "Tie"
        analysis.append("   🤝 TIE: Both algorithms performed equally well")
        analysis.append("   → Recommendation: Use A* for larger grids, BFS for small grids")
    
    analysis.append("=" * 60)
    
    return "\n".join(analysis), winner

def generate_detailed_explanation(algorithm, result, grid_info, safety_score, safety_message):
    """
    Generate detailed explanation of results with if-else logic
    
    Args:
        algorithm: name of algorithm used
        result: dictionary with algorithm results
        grid_info: dictionary with grid information
        safety_score: minimax/alpha-beta safety score
        safety_message: safety interpretation
    
    Returns:
        detailed explanation string
    """
    explanation = []
    explanation.append("=" * 60)
    explanation.append(f"🤖 INTELLIGENT EVACUATION AGENT REPORT")
    explanation.append(f"Algorithm: {algorithm}")
    explanation.append("=" * 60)
    
    # Grid Information
    explanation.append("\n🗺️ GRID ENVIRONMENT ANALYSIS")
    explanation.append("-" * 40)
    explanation.append(f"   Grid Size: {grid_info['rows']} x {grid_info['cols']}")
    explanation.append(f"   Total Cells: {grid_info['total_cells']}")
    explanation.append(f"   Obstacles: {len(grid_info['obstacles'])} ({grid_info['obstacle_percentage']:.1f}%)")
    explanation.append(f"   Fire Hazards: {len(grid_info['fires'])}")
    explanation.append(f"   Exit Points: {len(grid_info['goals'])}")
    
    # Pathfinding Result
    explanation.append("\n🚶 PATHFINDING RESULT")
    explanation.append("-" * 40)
    
    if result['success']:
        explanation.append(f"   ✅ PATH FOUND successfully!")
        explanation.append(f"   📏 Path Length: {result['path_length']} steps")
        explanation.append(f"   🔍 Nodes Explored: {result['nodes_explored']}")
        explanation.append(f"   ⏱️ Time Taken: {result['time_taken']:.5f} seconds")
        
        # Algorithm-specific insights
        if algorithm == "BFS":
            explanation.append("\n📌 BFS-SPECIFIC INSIGHTS:")
            explanation.append("   • Explores all directions equally (level by level)")
            explanation.append("   • Guarantees the shortest path in unweighted grid")
            explanation.append(f"  • Visited {result['nodes_explored']} nodes to find solution")
            
            if result['nodes_explored'] > grid_info['total_cells'] * 0.5:
                explanation.append("   • ⚠️ Explored >50% of grid - may be inefficient for large maps")
            else:
                explanation.append("   • ✅ Explored relatively few nodes - efficient for this grid")
                
        elif algorithm == "A*":
            explanation.append("\n📌 A*-SPECIFIC INSIGHTS:")
            explanation.append("   • Uses Manhattan distance heuristic to guide search")
            explanation.append("   • Prioritizes nodes closer to the goal")
            explanation.append(f"  • Explored {result['nodes_explored']} nodes with heuristic guidance")
            
            if result['nodes_explored'] < grid_info['total_cells'] * 0.3:
                explanation.append("   • ✅ Heuristic was very effective (explored <30% of grid)")
            else:
                explanation.append("   • ⚠️ Heuristic had moderate effectiveness")
    else:
        explanation.append("   ❌ NO PATH FOUND!")
        explanation.append("   → The goal is unreachable from the start position")
        explanation.append("   → Possible reasons: walls blocking all paths, disconnected regions")
    
    # Safety Analysis
    explanation.append("\n🔥 SAFETY & RISK ANALYSIS (Minimax + Alpha-Beta)")
    explanation.append("-" * 40)
    explanation.append(f"   Safety Score: {safety_score}")
    explanation.append(f"   Risk Level: {safety_message}")
    
    if safety_score <= -100:
        explanation.append("   🚨 IMMEDIATE DANGER! Current position is a fire location!")
        explanation.append("   → Agent must evacuate immediately!")
    elif safety_score <= -50:
        explanation.append("   ⚠️ HIGH RISK! Fire is very close to agent position")
        explanation.append("   → Agent should move away from fire direction")
    elif safety_score <= 0:
        explanation.append("   ⚠️ MODERATE RISK - Proceed with caution")
        explanation.append("   → Agent should prioritize moving toward exits")
    elif safety_score <= 30:
        explanation.append("   ✅ LOW RISK - Safe path available")
        explanation.append("   → Agent can proceed with normal evacuation")
    else:
        explanation.append("   🎯 EXCELLENT! Near exit or very safe position")
        explanation.append("   → Agent is close to safe evacuation point")
    
    # Recommendation
    explanation.append("\n💡 AGENT RECOMMENDATION")
    explanation.append("-" * 40)
    
    if result['success']:
        if safety_score < -50:
            explanation.append("   → EVACUATE IMMEDIATELY using the found path")
            explanation.append("   → Do NOT delay - fire hazard detected nearby")
        elif result['path_length'] > 10:
            explanation.append("   → Long evacuation path detected")
            explanation.append("   → Consider finding alternative exits if available")
        else:
            explanation.append("   → Safe evacuation path available")
            explanation.append("   → Follow the computed path to reach the exit")
    else:
        explanation.append("   → No safe path found from current position")
        explanation.append("   → Agent should seek alternative exit or call for help")
    
    explanation.append("=" * 60)
    
    return "\n".join(explanation)
