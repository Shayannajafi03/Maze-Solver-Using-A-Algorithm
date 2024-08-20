import heapq
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

def read_graph():
    number_of_rows = int(input("the number of rows?"))
    maze = []
    for i in range(number_of_rows):
        row = list(map(int, input(f"write the {i+1}th row").split()))
        maze.append(row)
    return maze

def neighborns(location, maze):
    #valid moves are vertical , horizontal and diagonal
    movements = [(0, 1), (0, -1), (1, 0), (-1, 0) , (1 , 1) , (1 , -1) , (-1 , 1) , (-1 , -1)]
    neighborns_ = []
    for movement in movements:
        row = location[0] + movement[0]
        column = location[1] + movement[1]
        if is_valid((row, column), maze):
            neighborns_.append((row, column))
    return neighborns_

def is_valid(point, maze):
    # check if it's a valid neighbor and there is a connection between them
    return 0 <= point[0] < len(maze) and 0 <= point[1] < len(maze[0]) and maze[point[0]][point[1]] == 1

def heuristics(point, goal):
    # use Euclidean distance as heuristic function   
    return sqrt((point[0] - goal[0])**2 + (point[1] - goal[1])**2)

def Astar(maze):
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)
    visited = set()
    frontier = []
    heapq.heappush(frontier, (0, [start]))
    g_costs = {start: 0}

    while frontier:
        _, path = heapq.heappop(frontier)
        current = path[-1]

        if current == end:
            print(len(frontier))
            return path  

        if current not in visited:
            neighborns_ = neighborns(current, maze)
            for neighbor in neighborns_:
                new_cost = g_costs[current] + 1
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    priority = new_cost + heuristics(neighbor, end)
                    heapq.heappush(frontier, (priority, path + [neighbor]))

            visited.add(current)

    return None


def show_maze(maze , path):
    
    fig, ax = plt.subplots(figsize=(7, 7))
    cmap = plt.cm.gray  # Use grayscale colors (0=black, 1=white)
    ax.imshow(maze, cmap=cmap, interpolation='none')

    #Add grid lines
    ax.set_xticks(np.arange(-0.5, len(maze[0]), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(maze), 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

    #Remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    #Plot the points
    for point in path:
        ax.scatter(point[1], point[0], color='red', s=150 , marker=".")  # Swap x and y to match imshow

    #Connect the points with lines
    x_coords, y_coords = zip(*[(point[1], point[0]) for point in path])  # Extract x and y separately
    ax.plot(x_coords, y_coords, color='green', linewidth=0.5)  # Connect the points
    fig.text(0.02, 0.02, f"cost = {len(path)-1}", ha='left', va='bottom', fontsize=12, color='black') # add the cost 

    # Display the plot
    plt.show()
    
    

"""maze =[ 
[ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 ],
[ 1, 1, 1, 0, 1, 1, 1, 0, 1, 1 ], 
[ 1, 1, 1, 0, 1, 1, 0, 1, 0, 1 ], 
[ 0, 0, 1, 0, 1, 0, 0, 0, 0, 1 ], 
[ 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 ], 
[ 1, 0, 1, 1, 1, 1, 0, 1, 0, 0 ], 
[ 1, 0, 0, 0, 0, 1, 0, 0, 0, 1 ], 
[ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 ], 
[ 1, 1, 1, 0, 0, 0, 1, 0, 0, 1 ] 
]
"""

if __name__ == "__main__":
    maze = read_graph()
    path = Astar(maze)
    if path:
        print(f"Shortest path found:{path} & cost of {len(path)-1}")
        show_maze(maze, path)
    else:
        print("there isn't any path to the end")