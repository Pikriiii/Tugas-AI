import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import PriorityQueue

def generate_maze(size):
    maze = np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])
    maze[1, 0] = 0  
    maze[size-1, size-1] = 0
    return maze

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == end:
            break

        for next in neighbors(maze, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                frontier.put(next, priority)
                came_from[next] = current

    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def neighbors(maze, current):
    row, col = current
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r = row + dr
        c = col + dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0:
            result.append((r, c))
    return result

def plot_maze_with_animation(maze, path=None):
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap='binary', vmin=0, vmax=1)
    ax.set_xticks(np.arange(-.5, maze.shape[1], 1))
    ax.set_yticks(np.arange(-.5, maze.shape[0], 1))
    ax.grid(which='both', color='black', linestyle='-', linewidth=1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.add_patch(plt.Rectangle((0-.5, 0-.5), 1, 1, fill=True, color='green', alpha=0.5))
    ax.add_patch(plt.Rectangle((maze.shape[1]-1-.5, maze.shape[0]-1-.5), 1, 1, fill=True, color='red', alpha=0.5))
    plt.title('Maze')

    if path:
        def update(frame):
            new_maze = np.where(maze == 1, 1, 0)  
            for step in frame:
                new_maze[step] = 3 
            ax.imshow(new_maze, cmap='RdGy_r', vmin=0, vmax=6, alpha=0.5)

        anim = FuncAnimation(fig, update, frames=path, interval=100, repeat=False)

    plt.show()

maze_size = 10
start = (0, 0)
end = (maze_size-1, maze_size-1)

while True:
    maze = generate_maze(maze_size)
    path = a_star(maze, start, end)
    if path:
        path_frames = [path[:i] for i in range(1, len(path)+1)]
        plot_maze_with_animation(maze, path_frames)
        break
    else:
        print("Tidak ada jalur yang menghubungkan titik awal dan titik akhir. Mencoba lagi...")
