from heapq import heappush, heappop
from algorithms.jps import calculate_total_dist
from graph import Graph, Node  # noqa # pylint: disable=unused-import


def a_star(start: tuple, goal: tuple, graph: Graph):
    """
    Implementaatio Dijkstran algoritmista.
    Argumentteina annetaan lähtö ja maali x,y -koordinaatit ja Graph-olio.
    Löydetty reitti täytetään Graph-olion visited attribuuttiin.
    """
    queue = []
    heappush(queue, (0, 0, start))
    graph.visited[start] = (0, start)
    # pylint:disable=duplicate-code
    # Verkon käsittely lähes sama kuin Dijkstran, mutta lasketaan etäisyyttä maaliin.
    while len(queue) > 0:
        _, distance, coords = heappop(queue)
        if goal == coords:
            break
        for _, neighbour in graph.nodes[coords].items():
            to_neighbour = distance + neighbour.dist
            if neighbour.obstacle or (
                neighbour.coords in graph.visited
                and graph.visited[neighbour.coords][0] <= to_neighbour
            ):
                continue
            graph.visited[neighbour.coords] = (to_neighbour, coords)
            cost = calculate_total_dist(neighbour.coords, goal, to_neighbour)
            heappush(queue, (cost, to_neighbour, neighbour.coords))
