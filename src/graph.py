class Node:
    """Solmu-luokka.
    Obstacle on True jos kyseessä on este ja False kun solmuun voidaan kulkea.
    Coordinates kertoo solmun x,y position pikselikartassa.
    """

    def __init__(self, obstacle: str, coordinates: tuple) -> None:
        self.obstacle = True
        if obstacle in [".", "G", "S"]:
            self.obstacle = False
        self.coords = coordinates
        self.pruned = False


class Graph:
    """Verkko-luokka.

    - nodes on sanakirja, missä (x,y)-koordinaatti on avain
    ja arvoina sanakirja suunnista (key) ja suunnan Node-olio naapurista (value).
    Suunnat on numeroitu 0-7
    myötäpäivään alkaen suoraan ylöspäin.
    - visited on sanakirja, missä (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja koordinaatti mistä
    avain-koordinaattiin on kuljettu.
    """

    DIRECTIONS = {
        0: (0, -1),
        1: (1, -1),
        2: (1, 0),
        3: (1, 1),
        4: (0, 1),
        5: (-1, 1),
        6: (-1, 0),
        7: (-1, -1),
    }

    def __init__(self, ascii_graph: list = None, remove_corner_cuts=True) -> None:
        self.nodes = {(int, int): {int: Node}}
        self.visited = {(int, int): (int, (int, int))}
        if ascii_graph is not None:
            self.generate_graph(ascii_graph, remove_corner_cuts)

    def reset_visited(self):
        """Apufunktio polunetsintä tulosten tyhjentämiseen,
        ilman että tarvitsee ladata uutta karttatietoa.
        """
        self.visited = {}

    def generate_graph(self, ascii_graph: list, remove_corner_cuts=True):
        """Muodostetaan Graph-olio taulukosta ASCII merkkejä.
        Merkkien oletetaan olevan Moving AI Labin materiaalin mukaisia:
        https://www.movingai.com/benchmarks/formats.html

        Args:
             ascii_graph (list): kaksiulotteinen lista ascii merkkejä.
        """
        self.nodes = {}
        self.reset_visited()

        for y, row in enumerate(ascii_graph):
            for x, col in enumerate(row):
                node = Node(col, (x, y))
                if node.obstacle:
                    continue
                self.nodes[node.coords] = {}
                for d, mod in self.DIRECTIONS.items():
                    neighbour_xy = (x + mod[0], y + mod[1])
                    if 0 <= neighbour_xy[0] < len(row) and 0 <= neighbour_xy[1] < len(
                        ascii_graph
                    ):
                        neighbour_node = Node(
                            ascii_graph[neighbour_xy[1]][neighbour_xy[0]],
                            neighbour_xy,
                        )
                        self.nodes[node.coords][d] = neighbour_node

                self.__remove_illegal_diagonal_vertices(node.coords, remove_corner_cuts)

    def __remove_illegal_diagonal_vertices(self, coords: tuple, remove_corner_cuts: bool):
        """Muodostetuista kaarista poistetaan ne, jotka kulkevat kahden esteen välistä tai
        leikkaavat esteen kulmaa, jos remove_corner_cuts on True.

        Args:
            coords (tuple): Solmun koordinaatit, jonka naapureita tarkastellaan. 
            remove_corner_cuts (bool): Jos remove_corner_cuts on True,
            poistetaan diagonaaliset kaaret, jotka leikaavat esteen kulmaa.
        """
        for direction in range(1, 8, 2):
            if direction not in self.nodes[coords]:
                continue
            prev_neighbour = direction - 1
            next_neighbour = 0 if direction == 7 else direction + 1
            if (
                prev_neighbour in self.nodes[coords]
                and next_neighbour in self.nodes[coords]
            ):
                if (
                    self.nodes[coords][prev_neighbour].obstacle
                    and self.nodes[coords][next_neighbour].obstacle
                ):
                    del self.nodes[coords][direction]
                    continue
            if remove_corner_cuts:
                if (
                    prev_neighbour in self.nodes[coords]
                    and self.nodes[coords][prev_neighbour].obstacle
                ):
                    del self.nodes[coords][direction]
                elif (
                    next_neighbour in self.nodes[coords]
                    and self.nodes[coords][next_neighbour].obstacle
                ):
                    del self.nodes[coords][direction]
