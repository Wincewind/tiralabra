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
        self.dist = 1


class Graph:
    """Verkko-luokka.

    - nodes on sanakirja, missä (x,y)-koordinaatti on avain
    ja arvoina sanakirja suunnista (key) ja suunnan Node-olio naapurista (value).
    Suunnat on numeroitu 0-7
    myötäpäivään alkaen suoraan ylöspäin.
    - visited on sanakirja, missä (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja koordinaatti mistä
    avain-koordinaattiin on kuljettu.
    - no_corner_cuts asetetaan joko True tai False generoidessa verkkoa ja siitä
    jps algoritmi voi tarkistaa, mitä suuntia sen pitää tarkistaa määrittääkseen
    "pakotettuja naapureita".
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
        self.no_corner_cuts = False
        if ascii_graph is not None:
            self.generate_graph(ascii_graph, remove_corner_cuts)

    def reset_visited(self):
        """Apufunktio polunetsintä tulosten tyhjentämiseen,
        ilman että tarvitsee ladata uutta karttatietoa.
        """
        self.visited = {}

    def reset_pruned(self):
        for _,neighbours in self.nodes.items():
            for _, n in neighbours.items():
                n.pruned = False

    def generate_graph(self, ascii_graph: list, remove_corner_cuts=True):
        """Muodostetaan Graph-olio taulukosta ASCII merkkejä.
        Merkkien oletetaan olevan Moving AI Labin materiaalin mukaisia:
        https://www.movingai.com/benchmarks/formats.html

        Args:
             ascii_graph (list): kaksiulotteinen lista ascii merkkejä.
        """
        def __generate_neighbours(node: Node):
            """Alifunktio solmun naapureiden generoimiseen."""
            for d, mod in self.DIRECTIONS.items():
                neighbour_xy = (x + mod[0], y + mod[1])
                if 0 <= neighbour_xy[0] < len(row) and 0 <= neighbour_xy[1] < len(
                    ascii_graph
                ):
                    neighbour_node = Node(
                        ascii_graph[neighbour_xy[1]][neighbour_xy[0]],
                        neighbour_xy,
                    )
                    if d % 2 != 0:
                        # Kuljettua matkaa täytetään vaaka tai pystysuunnassa
                        # yhdellä ja diagonaalisessa suunnassa kahden neliöjuurella
                        # 8 desimaalin tarkkuudella. Moving AI Labin skenaarioiden lyhyimmät
                        # polut on annettu tällä tarkkuudella, joten tällä pyritään saamaan
                        # mahdollisimman yhtenäisiä tuloksia.
                        neighbour_node.dist = 1.41421356
                    self.nodes[node.coords][d] = neighbour_node

        self.nodes = {}
        self.reset_visited()
        self.no_corner_cuts = remove_corner_cuts

        for y, row in enumerate(ascii_graph):
            for x, col in enumerate(row):
                node = Node(col, (x, y))
                if node.obstacle:
                    continue
                self.nodes[node.coords] = {}
                __generate_neighbours(node)
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
            if direction not in self.nodes[coords] or self.nodes[coords][direction].obstacle:
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
