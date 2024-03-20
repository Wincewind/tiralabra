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


class Graph:
    """Verkko-luokka.
    
    - nodes on sanakirja, missä (x,y)-koordinaatti on avain
    ja arvoina lista Node-olio naapureista ja suunnista. Suunnat on numeroitu 0-7
    myötäpäivään alkaen suoraan ylöspäin.
    - visited on sanakirja, missä (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja koordinaatti mistä
    avain-koordinaattiin on kuljettu.
    """

    def __init__(self,ascii_graph: list=None) -> None:
        self.nodes = {(int,int):[(Node,int)]}
        self.visited = {(int,int):(int,(int,int))}
        if ascii_graph is not None:
            self.generate_graph(ascii_graph)

    def reset_visited(self):
        """Apufunktio polunetsintä tulosten tyhjentämiseen,
        ilman että tarvitsee ladata uutta karttatietoa.
        """
        self.visited = {}

    def generate_graph(self, ascii_graph: list):
        """Muodostetaan Graph-olio taulukosta ASCII merkkejä.
        Merkkien oletetaan olevan Moving AI Labin materiaalin mukaisia:
        https://www.movingai.com/benchmarks/formats.html

        Args:
             ascii_graph (list): kaksiulotteinen lista ascii merkkejä.
        """
        self.nodes = {}
        self.reset_visited()
        directions = {
            0: (0, -1),
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            4: (0, 1),
            5: (-1, 1),
            6: (-1, 0),
            7: (-1, -1),
        }
        for y, row in enumerate(ascii_graph):
            for x, col in enumerate(row):
                node = Node(col, (x, y))
                if node.obstacle:
                    continue
                self.nodes[node.coords] = []
                for d, mod in directions.items():
                    neighbour_xy = (x + mod[0], y + mod[1])
                    if 0 <= neighbour_xy[0] < len(row) and 0 <= neighbour_xy[1] < len(
                        ascii_graph
                    ):
                        neighbour_node = Node(
                            ascii_graph[neighbour_xy[1]][neighbour_xy[0]],
                            neighbour_xy,
                        )
                        self.nodes[node.coords].append((neighbour_node, d))
