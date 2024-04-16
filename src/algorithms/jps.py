from math import sqrt
from heapq import heappush
from graph import Graph

SURROUNDING_DIRECTIONS = {0:(7,1),
                          1:(0,2),
                          2:(1,3),
                          3:(2,4),
                          4:(3,5),
                          5:(4,6),
                          6:(5,7),
                          7:(6,0)}


def calculate_total_dist(current_node: tuple, target_node: tuple, dist_traveled=0):
    a, b = abs(current_node[0] - target_node[0]), abs(current_node[1] - target_node[1])
    return dist_traveled + sqrt(a * a + b * b)


def _identify_successors(transition: tuple, goal: tuple, graph: Graph) -> list:
    """Toteutus JPS:n julkaisun algoritmin 1 funktion pseudokoodista. Tarkoituksena on
    ensin karsia nykyisestä solmusta naapurit yhtä kaarta aiemman solmun ja kuljettavan
    suunnan perusteella. Tämän jälkeen jäljellä olevista naapureista lähdetään
    etsimään seuraavaa hyppypistettä.

    Args:
        transition (tuple): yhtä kaarta aiempi solmu, kuljettu suunta ja nykyinen solmu.
        goal (tuple): Maali solmu. Yksi mahdollisista hyppypisteistä.
        graph (Graph): Verkko-olio.

    Returns:
        list: Löydetyt hyppypisteet.
    """
    successors = []
    prev_node, direction, current_node = transition
    if prev_node is not None:
        _prune(prev_node, direction, current_node, graph)
    for d, _ in graph.nodes[current_node].items():
        jump_point = _jump(current_node, d, goal, graph)
        if jump_point[0] is not None:
            successors.append(jump_point)
    return successors


def _jump(
    current_node: tuple, direction: int, goal: tuple, graph: Graph, dist_to_node=0
) -> tuple:
    """Toteutus JPS:n julkaisun algoritmin 2 funktion pseudokoodista.
    Rekursiivisessa funktiossa tarkistetaan solmuja edeten tiettyyn suuntaan,
    kunnes löydetään hyppypiste.

    Args:
        current_node (tuple): Hyppypistettä edeltävä solmu.
        direction (int): Suunta mistä ollaan tulossa.
        goal (tuple): Maali-solmun x,y-koordinaatit, koska tämä on yksi mahdollinen hyppypiste.
        graph (Graph): Verkko-olio
        dist_to_node (int, optional): Tähän asti kuljettu matka aiemmasta
        hyppypisteestä nykyiseen tarkasteltavaan solmuun. Oletusarvona 0.

    Returns:
        tuple(tuple,float,int): Hyppypistettä edeltävän solmun ja itse
        hyppypisteen koordinaatit tuplena, kuljettu matka aiemman hyppypisteen
        ja löydetyn välillä sekä hyppypisteen ja edeltävän solmun kaaren suunta.
        Jos hyppypistettä ei löydy, palautetaan (None,0,-1).
    """
    node = None
    try:
        node = graph.nodes[current_node][direction]
    except KeyError:
        return None, 0, -1
    if node.obstacle or node.pruned:
        return None, 0, -1
    if node.coords == goal:
        return (current_node, node.coords), dist_to_node + node.dist, direction
    if _check_for_forced_neighbours(
        current_node, direction, node.coords, graph, [], True
    ):
        return (current_node, node.coords), dist_to_node + node.dist, direction

    if direction % 2 != 0:
        directions = SURROUNDING_DIRECTIONS[direction]
        for d in directions:
            if (
                _jump(node.coords, d, goal, graph, dist_to_node + node.dist)[0]
                is not None
            ):
                return (current_node, node.coords), dist_to_node + node.dist, direction
    return _jump(node.coords, direction, goal, graph, dist_to_node + node.dist)

def _set_forced_neighbour_directions(direction: int, graph: Graph):
    """Palauttaa annetun suunnan ympäröivät suunnat, joissa olevien
    solmujen osalta päätellään, onko nykyinen solmu "pakoitettu naapuri".

    Args:
        direction (int): Suunta josta ollaan tultu
        graph (Graph): Verkko-olio

    Returns:
        tuple: annettua suuntaa edeltävä ja seuraava suunta tai
        jos kulmien leikkaus ei ole sallittua, edeltävää edeltävä ja seuraavaa seuraava suuunta.
    """
    prev_neighbour, next_neighbour = SURROUNDING_DIRECTIONS[direction]
    if graph.no_corner_cuts and direction % 2 == 0:
        prev_neighbour = SURROUNDING_DIRECTIONS[prev_neighbour][0]
        next_neighbour = SURROUNDING_DIRECTIONS[next_neighbour][1]
    return prev_neighbour, next_neighbour

def _check_for_forced_neighbours(
    prev_node: tuple,
    direction: int,
    node_to_check: tuple,
    graph: Graph,
    directions_to_prune: list,
    only_check_for_forced=False,
):
    """Jos tarkasteltavalla naapurilla ja current_nodella on esteitä yhteisinä naapureina,
        tulee tiettyjen suuntien siirtymistä ns. "pakotettuja". Nämä tilanteet on nähtävissä
        JPS julkaisun kuvista 2 a-d.

    Args:
        prev_node (tuple): Solmun x,y-koordinaatit, josta ollaan tultu nykyiseen solmuun.
        direction (int): Suunta (0-7), mistä ollaan tultu.
        node_to_check (tuple): Nykyisen solmun x,y-koordinaatit.
        graph (Graph): Verkko-olio.
        directions_to_prune (list): Karsittavat naapurien suunnat.
        Jos suunnassa on pakotettu naapuri, se poistetaan listalta.
        only_check_for_forced (bool, optional): True jos halutaan vaan tieto onko nykyisellä
        solmulla pakotettuja naapureita. Oletusarvo on False.

    Returns:
        bool || directions_to_prune: Jos only_check_for_forced == True
        ja halutaan tarkistaa vain pakotetut naapurit, palautetaan välittömästi
        True jos löytyy pakotettu naapuri, muuten False.
        Jos only_check_for_forced == False, palautetaan päivitetty directions_to_prune lista.
    """
    prev_neighbour, next_neighbour = _set_forced_neighbour_directions(direction, graph)
    for d, get_prev_neighbour in ((prev_neighbour, True), (next_neighbour, False)):
        if direction % 2 != 0:
            if not only_check_for_forced:
                directions_to_prune.remove(d)
        if (
            d in graph.nodes[prev_node]
            and graph.nodes[prev_node][d].obstacle
            and d in graph.nodes[node_to_check]
            and not graph.nodes[node_to_check][d].obstacle
            and graph.nodes[node_to_check][d].coords != prev_node
        ):
            if direction % 2 != 0:
                prev_d, next_d = SURROUNDING_DIRECTIONS[d]
                forced_d = prev_d if get_prev_neighbour else next_d
                if only_check_for_forced:
                    return True
                directions_to_prune.remove(forced_d)
            else:
                if only_check_for_forced:
                    return True
                directions_to_prune.remove(d)
                if graph.no_corner_cuts and get_prev_neighbour:
                    directions_to_prune.remove(SURROUNDING_DIRECTIONS[d][1])
                elif graph.no_corner_cuts:
                    directions_to_prune.remove(SURROUNDING_DIRECTIONS[d][0])
    if only_check_for_forced:
        return False
    return directions_to_prune


def _prune(prev_node: tuple, direction: int, node_to_check: tuple, graph: Graph):
    """Funktio karsimaan viereisen solmun naapurit, joista lähdetään etsimään current_nodelle
    hyppypistettä. Tarkempi kuvaus strategian teoriasta löytyy JPS alkuperäisen julkaisun
    sivuilta 1115-1116.

    Args:
        prev_node (tuple): Solmun koordinaatit, mistä siirrytty naapuriin.
        direction (int): Suunta, mihin ollaan menossa.
        node_to_check (tuple): Naapuri-solmu, jonka naapureita ollaan karsimassa.
        graph (Graph): Verkko-olio, jossa kummankin tarkasteltavista solmuista naapurien tiedot.
    """
    directions_to_prune = list(range(8))
    # Pituus prev_nodesta samaan suuntaan kun ollaan jo menossa tulee
    # aina olemaan pidempi (jos ei kuljeta node_to_check kautta), joten tätä ei karsita.
    directions_to_prune.remove(direction)
    directions_to_prune = _check_for_forced_neighbours(
        prev_node, direction, node_to_check, graph, directions_to_prune
    )
    for d in directions_to_prune:
        if d in graph.nodes[node_to_check]:
            graph.nodes[node_to_check][d].pruned = True


def _update_visited_and_queue(
    prev_jump_point: tuple,
    prev_node_and_jp: tuple,
    dist_to_jump_point: float,
    direction: int,
    goal: tuple,
    graph: Graph,
    queue: list,
):
    """Viedään löydettyjen hyppypisteiden tiedot jonoon ja Graph-olion visited-sanakirjaan.

    Args:
        prev_jump_point (tuple): Aiemman hyppypiste solmun x,y-koordinaatit. "Polku muodostuu
        tämän ja seuraavan hyppypisteen välille.
        prev_node_and_jp (tuple): Hyppypiste solmun ja sitä aiemman solmun x,y-koordinaatit.
        prev_node tarvitaan kun hyppypisteestä seuraavia solmuja aletaan etsiä
        ja sen naapurit karsitaan.
        dist_to_jump_point (float): Etäisyys prev_jump_point ja nykyisen hyppypisteen välillä.
        direction (int): Suunta, mistä nykyiseen hyppypisteeseen ollaan tulossa.
        goal (tuple): Maalin x,y-koordinaatit. Käytetään laskemaan etäisyys
        uuden hyppypisteen ja maalin välillä.
        graph (Graph): Verkko-olio.
        queue (list): Binäärikeko lista, johon seuraavan hyppypisteen tiedot lisätään muodossa
        (kuljettu etäisyys hyppypisteeseen + suora etäisyys maaliin, kuljettu etäisyys
        hyppypisteeseen, (hyppypistettä aiempi solmu, suunta hyppypisteeseen, hyppypiste)).
    """
    prev_node, node = prev_node_and_jp
    if node not in graph.visited or graph.visited[node][0] > dist_to_jump_point:
        cost = calculate_total_dist(node, goal, dist_to_jump_point)
        heappush(queue, (cost, dist_to_jump_point, (prev_node, direction, node)))
        graph.visited[node] = (dist_to_jump_point, prev_jump_point)


def jps(start: tuple, goal: tuple, graph: Graph):
    """Jump point search algoritmi, joka etsii lyhyintä
    polkua start ja goal välillä graph verkossa.
    Perustuu Harabor, D. ja Grastien, A (2011) julkaisuun aiheesta.

    Args:
        start (tuple): Lähdön x,y-koordinaatit.
        goal (tuple): Maalin x,y-koordinaatit.
        graph (Graph): Verkko-olio
    """
    graph.queue.append((0, 0, (None, -1, start)))
    graph.visited[start] = (0, start)
    while len(graph.queue) > 0:
        _, distance, transition = graph.queue_pop()
        if goal == transition[2]:
            break
        successors = _identify_successors(transition, goal, graph)
        for prev_node_and_jp, dist_to_jp, direction in successors:
            dist_to_jp += distance
            _update_visited_and_queue(
                transition[2],
                prev_node_and_jp,
                dist_to_jp,
                direction,
                goal,
                graph,
                graph.queue,
            )
