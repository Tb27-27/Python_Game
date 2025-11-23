# src/pathfinding.py  (or put inside enemy.py for now)
import heapq

def a_star(start, goal, walls, tile_size=48, grid_width=100, grid_height=100):
    """
    A* pathfinding op een grid.
    """
    # Converteer naar grid coördinaten
    def world_to_grid(x, y):
        return int(x // tile_size), int(y // tile_size)
    
    def grid_to_world(gx, gy):
        return gx * tile_size + tile_size // 2, gy * tile_size + tile_size // 2

    start_gx, start_gy = world_to_grid(start[0], start[1])
    goal_gx, goal_gy = world_to_grid(goal[0], goal[1])

    # Maak een set van bezette grid cellen
    occupied = set()
    for wall in walls:
        wx, wy, ww, wh = wall
        gx = int(wx // tile_size)
        gy = int(wy // tile_size)
        gw = int(ww / tile_size) + 1
        gh = int(wh / tile_size) + 1
        for ox in range(gw):
            for oy in range(gh):
                occupied.add((gx + ox, gy + oy))

    # A* setup
    open_set = []
    heapq.heappush(open_set, (0 + manhattan((start_gx, start_gy), (goal_gx, goal_gy)), 0, (start_gx, start_gy)))
    
    came_from = {}
    g_score = { (start_gx, start_gy): 0 }
    visited = set()

    directions = [(0,1),(1,0),(0,-1),(-1,0), (1,1),(1,-1),(-1,1),(-1,-1)]  # 8-richting voor vloeiender pad

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == (goal_gx, goal_gy):
            # Reconstruct path
            path = []
            while current in came_from:
                wx, wy = grid_to_world(*current)
                path.append((wx, wy))
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path[1:] if len(path) > 1 else []  # skip start positie

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor[0] < 0 or neighbor[0] >= grid_width or neighbor[1] < 0 or neighbor[1] >= grid_height:
                continue
            if neighbor in occupied:
                continue
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + (1.4 if dx != 0 and dy != 0 else 1)  # diag kost meer

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan(neighbor, (goal_gx, goal_gy))
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None  # geen pad gevonden

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])