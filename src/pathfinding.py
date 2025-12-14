# src/pathfinding.py
import heapq

def a_star(start_pos, goal_pos, walls, tile_size=48, grid_width=100, grid_height=100):
    """
    A* pathfinding op een grid met duidelijke variabelenamen.
    """
    
    # hulp methods
    def world_to_grid(world_x, world_y):
        """Van pixel-coördinaten naar grid-index (rij/kolom)."""
        return int(world_x // tile_size), int(world_y // tile_size)
    
    def grid_to_world(grid_x, grid_y):
        """Van grid-index naar het midden van de tegel in pixels."""
        center_offset = tile_size // 2
        return grid_x * tile_size + center_offset, grid_y * tile_size + center_offset

    # start en richting
    start_grid_x, start_grid_y = world_to_grid(start_pos[0], start_pos[1])
    goal_grid_x, goal_grid_y = world_to_grid(goal_pos[0], goal_pos[1])
    goal_node = (goal_grid_x, goal_grid_y)

    # muren
    occupied_tiles = set()
    
    for wall in walls:
        # De rect van de muur in pixels
        wall_x, wall_y, wall_width, wall_height = wall
        
        # Bereken welke grid-vakjes deze muur bedekt
        start_tile_x = int(wall_x // tile_size)
        start_tile_y = int(wall_y // tile_size)
        
        # Hoeveel tegels breed en hoog is deze muur?
        tiles_wide = int(wall_width / tile_size) + 1
        tiles_high = int(wall_height / tile_size) + 1
        
        # Voeg al deze tegels toe aan de bezette set
        for offset_x in range(tiles_wide):
            for offset_y in range(tiles_high):
                occupied_tiles.add((start_tile_x + offset_x, start_tile_y + offset_y))

    # A* Algoritme
    open_set = []
    
    start_h_score = manhattan((start_grid_x, start_grid_y), goal_node)
    heapq.heappush(open_set, (0 + start_h_score, 0, (start_grid_x, start_grid_y)))
    
    came_from = {}
    g_score = { (start_grid_x, start_grid_y): 0 }
    visited = set()

    directions = [
        # Recht
        (0, 1), (1, 0), (0, -1), (-1, 0),
        # Diagonaal  
        (1, 1), (1, -1), (-1, 1), (-1, -1) 
    ]

    while open_set:
        # Haal de node met de laagste F-score op
        # de f score bepaald hoe ver iets is
        # lager is dus beter

        _, current_g, current_node = heapq.heappop(open_set)
        
        if current_node in visited:
            continue
        visited.add(current_node)

        # Doel bereikt?
        if current_node == goal_node:
            # Pad maken
            path = []
            while current_node in came_from:
                # grid weer omzetten naar map pexels
                world_x, world_y = grid_to_world(*current_node)
                path.append((world_x, world_y))
                current_node = came_from[current_node]
            
            # startpunt
            path.append(start_pos) 
            path.reverse()
            
            # geef pad terug
            return path[1:] if len(path) > 1 else []

        # buren check
        current_x, current_y = current_node
        
        for dx, dy in directions:
            neighbor_node = (current_x + dx, current_y + dy)
            neighbor_x, neighbor_y = neighbor_node

            # 1. check grenzen
            if not (0 <= neighbor_x < grid_width and 0 <= neighbor_y < grid_height):
                continue
            
            # 2. check muur
            if neighbor_node in occupied_tiles:
                continue
            
            # heck of we er al geweest
            if neighbor_node in visited:
                continue

            # Kosten berekenen: 1.4 voor diagonaal (wortel 2), 1.0 voor recht
            move_cost = 1.4 if dx != 0 and dy != 0 else 1.0
            tentative_g = g_score[current_node] + move_cost

            if neighbor_node not in g_score or tentative_g < g_score[neighbor_node]:
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g
                
                f_score = tentative_g + manhattan(neighbor_node, goal_node)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor_node))

    # geen pad gevonden dus niets doen
    return None  

def manhattan(point_a, point_b):
    """Bereken afstand tussen twee grid-punten (x1, y1) en (x2, y2)."""
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])