from math import sqrt
from graph import Graph

SUCCESSORS = {}
NEIGHBOURS = {}

def calculate_total_dist(current_node: tuple, target_node: tuple, dist_traveled=0):
    a,b = abs(current_node[0]-target_node[0]), abs(current_node[1]-target_node[1])
    return dist_traveled + sqrt(a**2+b**2)

# def jps(start: tuple, goal: tuple, graph: Graph):
#     global NEIGHBOURS
#     NEIGHBOURS = graph.nodes

# def identify_successors(current_node: tuple, start: tuple, goal: tuple):
#     global SUCCESSORS
#     SUCCESSORS[current_node] = None


# def jump(initial_node: tuple, direction: int, start: tuple, goal: tuple):
#     n = step(initial_node, direction)

# def step(node, direction):
#     neighbour =  [n for n, d in NEIGHBOURS[node] if d == direction]
#     if len(neighbour) == 0:
#         return None
#     return neighbour[0]

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
    # Pituus current_nodesta samaan suuntaan kun ollaan jo menossa tulee
    # aina olemaan pidempi, joten tätä ei karsita.
    directions_to_prune.remove(direction)

    prev_neighbour = direction - 1
    next_neighbour = 0 if direction == 7 else direction + 1
    for d, mod in ((prev_neighbour,-1),(next_neighbour,1)):
        # Jos tarkasteltavalla naapurilla ja current_nodella onesteitä yhteisinä naapureina,
        # tulee tiettyjen suuntien siirtymistä ns. "pakotettuja". Nämä tilanteet on nähtävissä
        # JPS julkaisun kuvista 2 a-d,
        if direction % 2 != 0:
            directions_to_prune.remove(d)
        if d in graph.nodes[current_node] and graph.nodes[current_node][d].obstacle:
            if direction % 2 != 0:
                forced_d =  d + mod
                forced_d = 7 if forced_d == -1 else forced_d
                forced_d = 0 if forced_d == 8 else forced_d
                directions_to_prune.remove(forced_d)
            else:
                directions_to_prune.remove(d)

    for d in directions_to_prune:
        if d in graph.nodes[node_to_check.coords]:
            graph.nodes[node_to_check.coords][d].pruned = True
