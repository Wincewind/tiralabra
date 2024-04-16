from heapq import heappush
from graph import Graph, Node  # noqa # pylint: disable=unused-import
# Node importataan tässä, jotta sen itellisense:iin päästään koodissa käsiksi.


def dijkstra(start: tuple, goal: tuple, graph: Graph):
    """
    Implementaatio Dijkstran algoritmista.
    Argumentteina annetaan lähtö ja maali x,y -koordinaatit ja Graph-olio.
    Löydetty reitti täytetään Graph-olion visited attribuuttiin.
    """
    heappush(graph.queue, (0, start))
    graph.visited[start] = (0, start)
    while len(graph.queue) > 0:
        distance, coords = graph.queue_pop()
        if goal == coords:
            break
        for _, neighbour  in graph.nodes[coords].items():
            to_neighbour = distance + neighbour.dist
            if neighbour.obstacle or (
                neighbour.coords in graph.visited
                and graph.visited[neighbour.coords][0] <= to_neighbour
            ):
                continue
            graph.visited[neighbour.coords] = (to_neighbour, coords)
            heappush(graph.queue, (to_neighbour, neighbour.coords))
