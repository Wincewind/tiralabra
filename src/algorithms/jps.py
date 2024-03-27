from math import sqrt
from heapq import heappop, heappush
from graph import Graph


def calculate_surrounding_directions(direction: int):
    prev_direction = 7 if direction - 1 == -1 else direction - 1
    next_direction = 0 if direction == 7 else direction + 1
    return prev_direction, next_direction


def calculate_total_dist(current_node: tuple, target_node: tuple, dist_traveled=0):
    a, b = abs(current_node[0] - target_node[0]), abs(current_node[1] - target_node[1])
    return dist_traveled + sqrt(a**2 + b**2)


def _identify_successors(current_node: tuple, start: tuple, goal: tuple, graph: Graph):
    successors = []
    for neighbour in graph.nodes[current_node].items():
        jump_point = _jump(current_node, neighbour[0], start, goal, graph)
        if jump_point is not None:
            successors.append(jump_point)
    return successors


def _jump(current_node: tuple, direction: int, start: tuple, goal: tuple, graph: Graph):
    node = None
    try:
        node = graph.nodes[current_node][direction]
    except KeyError:
        return None
    if node.obstacle or node.pruned:
        return None
    if node.coords == goal:
        return node
    if _prune(current_node, direction, graph):
        return node

    surrounding_directions = calculate_surrounding_directions(direction)
    if direction % 2 != 0:
        for d in surrounding_directions:
            if _jump(node.coords, d, start, goal, graph) is not None:
                return node
    return _jump(node.coords, direction, start, goal, graph)


def _prune(current_node: tuple, direction: int, graph: Graph):
    """Funktio karsimaan viereisen solmun naapurit, joista lähdetään etsimään current_nodelle
    hyppypistettä. Tarkempi kuvaus strategian teoriasta löytyy JPS alkuperäisen julkaisun
    sivuilta 1115-1116.

    Args:
        current_node (tuple): Solmun koordinaatit, mistä siirrytty naapuriin.
        direction (int): Suunta, mihin ollaan menossa.
        graph (Graph): Verkko-olio, jossa kummankin tarkasteltavista solmuista naapurien tiedot.
    """
    forced_neighbour = False
    node_to_check = graph.nodes[current_node][direction]
    directions_to_prune = list(range(8))
    # Pituus current_nodesta samaan suuntaan kun ollaan jo menossa tulee
    # aina olemaan pidempi, joten tätä ei karsita.
    directions_to_prune.remove(direction)
    prev_neighbour, next_neighbour = calculate_surrounding_directions(direction)
    for d, mod in ((prev_neighbour, -1), (next_neighbour, 1)):
        # Jos tarkasteltavalla naapurilla ja current_nodella on esteitä yhteisinä naapureina,
        # tulee tiettyjen suuntien siirtymistä ns. "pakotettuja". Nämä tilanteet on nähtävissä
        # JPS julkaisun kuvista 2 a-d.
        if direction % 2 != 0:
            directions_to_prune.remove(d)
        if (
            d in graph.nodes[current_node]
            and graph.nodes[current_node][d].obstacle
            and d in graph.nodes[node_to_check.coords]
            and not graph.nodes[node_to_check.coords][d].obstacle
            and graph.nodes[node_to_check.coords][d].coords != current_node
        ):
            if direction % 2 != 0:
                forced_d = d + mod
                forced_d = 7 if forced_d == -1 else forced_d
                forced_d = 0 if forced_d == 8 else forced_d
                directions_to_prune.remove(forced_d)
                forced_neighbour = True
            else:
                directions_to_prune.remove(d)
                forced_neighbour = True
    for d in directions_to_prune:
        if d in graph.nodes[node_to_check.coords]:
            graph.nodes[node_to_check.coords][d].pruned = True
    return forced_neighbour


def _update_visited_and_queue(prev_node, distance, node, goal, graph, queue):
    dist_to_jump_point = calculate_total_dist(prev_node, node.coords, distance)
    cost = calculate_total_dist(node.coords, goal, dist_to_jump_point)
    if node.coords in graph.visited:
        if graph.visited[node.coords][0] > dist_to_jump_point:
            try:
                prev_item = [
                    item for item in enumerate(queue) if item[2] == node.coords
                ]
                queue.remove(prev_item)
            except IndexError:
                pass
            heappush(queue, (cost, dist_to_jump_point, node.coords))
            graph.visited[node.coords] = (dist_to_jump_point, prev_node)
    else:
        heappush(queue, (cost, dist_to_jump_point, node.coords))
        graph.visited[node.coords] = (dist_to_jump_point, prev_node)


def jps(start: tuple, goal: tuple, graph: Graph):
    queue = []
    queue.append((0, 0, start))
    graph.visited[start] = (0, start)
    while len(queue) > 0:
        _, distance, coords = heappop(queue)
        if goal == coords:
            break
        successors = _identify_successors(coords, start, goal, graph)
        for n in successors:
            _update_visited_and_queue(coords, distance, n, goal, graph, queue)
