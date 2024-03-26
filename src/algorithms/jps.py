from math import sqrt
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
        _prune(current_node, neighbour, graph)
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
    surrounding_directions = calculate_surrounding_directions(direction)
    for d in surrounding_directions:
        if (
            d in graph.nodes[current_node]
            and graph.nodes[current_node][d].obstacle
            and d in graph.nodes[node.coords]
            and not graph.nodes[node.coords][d].obstacle
        ):
            return node
    if direction % 2 != 0:
        for d in surrounding_directions:
            if _jump(node.coords, d, start, goal, graph) is not None:
                return node
    return _jump(node.coords, direction, start, goal, graph)


def _prune(current_node: tuple, neighbour_to_check: tuple, graph: Graph):
    """Funktio karsimaan viereisen solmun naapurit, joista lähdetään etsimään current_nodelle
    hyppypistettä. Tarkempi kuvaus strategian teoriasta löytyy JPS alkuperäisen julkaisun
    sivuilta 1115-1116.

    Args:
        current_node (tuple): Solmun koordinaatit, mistä siirrytty naapuriin.
        neighbour_to_check (tuple): Suunta, mistä naapurisolmuun on tultu ja solmun Node-olio.
        graph (Graph): Verkko-olio, jossa kummankin tarkasteltavista solmuista naapurien tiedot.
    """
    directions_to_prune = list(range(8))
    direction, node_to_check = neighbour_to_check
    if node_to_check.obstacle:
        return
    # Pituus current_nodesta samaan suuntaan kun ollaan jo menossa tulee
    # aina olemaan pidempi, joten tätä ei karsita.
    directions_to_prune.remove(direction)

    prev_neighbour, next_neighbour = calculate_surrounding_directions(direction)
    for d, mod in ((prev_neighbour, -1), (next_neighbour, 1)):
        # Jos tarkasteltavalla naapurilla ja current_nodella on esteitä yhteisinä naapureina,
        # tulee tiettyjen suuntien siirtymistä ns. "pakotettuja". Nämä tilanteet on nähtävissä
        # JPS julkaisun kuvista 2 a-d,
        if direction % 2 != 0:
            directions_to_prune.remove(d)
        if (
            d in graph.nodes[current_node]
            and graph.nodes[current_node][d].obstacle
            and d in graph.nodes[node_to_check.coords]
            and not graph.nodes[node_to_check.coords][d].obstacle
        ):
            # if d in graph.nodes[current_node] and graph.nodes[current_node][d].obstacle:
            if direction % 2 != 0:
                forced_d = d + mod
                forced_d = 7 if forced_d == -1 else forced_d
                forced_d = 0 if forced_d == 8 else forced_d
                directions_to_prune.remove(forced_d)
            else:
                directions_to_prune.remove(d)

    for d in directions_to_prune:
        if d in graph.nodes[node_to_check.coords]:
            graph.nodes[node_to_check.coords][d].pruned = True


# def jps(start: tuple, goal: tuple, graph: Graph):
#     global NEIGHBOURS
#     NEIGHBOURS = graph.nodes
