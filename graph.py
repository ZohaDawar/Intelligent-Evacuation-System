import matplotlib.pyplot as plt

def plot_algorithm_comparison(bfs_result, astar_result):
    algorithms = ["BFS", "A*"]

    times = [
        bfs_result["time_taken"],
        astar_result["time_taken"]
    ]

    nodes = [
        bfs_result["nodes_explored"],
        astar_result["nodes_explored"]
    ]

    # Time comparison graph
    plt.figure()
    plt.title("Time Comparison")
    plt.bar(algorithms, times)
    plt.xlabel("Algorithm")
    plt.ylabel("Time (seconds)")
    plt.show()

    # Nodes explored graph
    plt.figure()
    plt.title("Nodes Explored Comparison")
    plt.bar(algorithms, nodes)
    plt.xlabel("Algorithm")
    plt.ylabel("Nodes Explored")
    plt.show()
