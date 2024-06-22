import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Maze:
    def __init__(self, maze, start, end):
        self.maze = np.array(maze)
        self.size = self.maze.shape[0]  
        self.start = start  
        self.goal = end 

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self):
        open_list = set([self.start])
        closed_list = set()
        g_cost = {self.start: 0}
        parents = {self.start: None}

        while open_list:
            current = min(open_list, key=lambda o: g_cost[o] + self.heuristic(o, self.goal))
            if current == self.goal:
                path = []
                while current:
                    path.append(current)
                    current = parents[current]
                path.reverse()
                return path

            open_list.remove(current)
            closed_list.add(current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < self.size and 0 <= neighbor[1] < self.size and
                        self.maze[neighbor] == 0 and neighbor not in closed_list):
                    tentative_g_cost = g_cost[current] + 1
                    if neighbor not in open_list or tentative_g_cost < g_cost.get(neighbor, float('inf')):
                        parents[neighbor] = current
                        g_cost[neighbor] = tentative_g_cost
                        open_list.add(neighbor)
        return None

    def animate_solution(self, path):
        fig, ax = plt.subplots()
        ax.imshow(self.maze, cmap='binary')
        ax.set_xticks([])
        ax.set_yticks([])
        line, = ax.plot([], [], 'ro-')  # Red line for the path

        def init():
            line.set_data([], [])
            return line,

        def animate(i):
            if i < len(path):
                x, y = zip(*path[:i+1])
                line.set_data(y, x)
            return line,

        anim = FuncAnimation(fig, animate, init_func=init, frames=len(path)+1, interval=500, blit=True)
        plt.show()

# Example usage:
maze_pattern = [
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
]

maze = Maze(maze_pattern,(15, 0),(0, 15))
path = maze.a_star_search()

if path:
    print(path)
    maze.animate_solution(path)
else:
    print("No path found.")
