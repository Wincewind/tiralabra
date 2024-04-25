import os
from math import cos, sin, floor
import matplotlib.pyplot as plt
from PIL import Image


class GifGenerator:
    def __init__(
        self, map_name: str, dimensions: tuple, generate_gif: bool = False
    ) -> None:
        self.generate_gif = generate_gif
        self.map_name = map_name
        self.scen = None
        self.algorithm = "dijkstra"
        self.base_img = form_base_img(map_name, dimensions)
        self.images = []
        self._round_counter = 0

    def set_run_parameters(self, scen: dict, algorithm: str):
        """Nollataan ja asetetaan ajettavan skenaarion tiedot
        uuden animaation muodostamista varten.

        Args:
            scen (dict): Skenaarion tiedot sanakirjassa.
            algorithm (str): Algoritmin nimi, jolla polkua etsitään.
        """
        self.images = []
        self._round_counter = 0
        self.scen = scen
        self.algorithm = algorithm

    def generate_new_image(self, next_queue_item, nodes, visited):
        """Muodostetaan uusi kuva gif-animaatioon. Polun muodostamisen
        tilannetta ei piirretä jokaisen solmun kohdalla vaan joka viides
        solmu jps:llä ja dijkstralla A*:lla vaihdellen riippuen lyhyimmän
        polun pituudesta.

        Args:
            next_queue_item (tuple): Algoritmin keon seuraava pienimmän
            etäisyyden/hinnan solmu.
            nodes (dict): Verkon solmut vieruslistana.
            visited (dict): Sanakirja käsiteltyjä solmuja, mistä voidaan
            muodostaa algoritmin löytämä reitti.
        """
        self._round_counter += 1
        if self.algorithm == "jps":
            end = next_queue_item[-1][-1]
        else:
            end = next_queue_item[-1]
        if (
            self.algorithm == "jps" or (self.scen["shortest"] > 1000 and self._round_counter == 5)
        ) or self._round_counter > self.scen["shortest"] / 2:
            self.images.append(
                draw_path_onto_map(
                    (self.scen["start"], end),
                    self.scen["goal"],
                    self.algorithm,
                    nodes,
                    visited,
                    self.base_img.copy(),
                )
            )
            self._round_counter = 0


def create_gif(gifgen: GifGenerator, nodes: dict, visited: dict):
    """Lisätään animaatioon kuva lopullisesta löydetystä polusta ja muodostetaan animaatio.

    Args:
        gifgen (GifGenerator): GifGenerator-olio.
        nodes (dict): Verkon solmut vieruslistana viimeistä kuvaa varten.
        visited (dict): Sanakirja käsiteltyjä solmuja, mistä voidaan
            muodostaa algoritmin löytämä reitti.
    """
    gifgen.images.append(
        draw_path_onto_map(
            (gifgen.scen["start"], gifgen.scen["goal"]),
            gifgen.scen["goal"],
            gifgen.algorithm,
            nodes,
            visited,
            gifgen.base_img.copy(),
        )
    )
    gifgen.images[0].save(
        f"output/{gifgen.map_name}_{str(gifgen.scen['index'])}_{gifgen.algorithm}.gif",
        save_all=True,
        append_images=gifgen.images[1:],
        optimize=False,
        duration=100,
    )


def display_formed_img(map_name: str, scen_index: int, algorithm: str):
    """Avaa suorituksen tuloksena muodostetun kuvan."""
    img = plt.imread(f"output/{map_name}_{scen_index}_{algorithm}.png")
    plt.imshow(img)
    plt.pause(10)


def display_formed_gif(map_name: str, scen_index: int, algorithm: str):
    """Avaa suorituksen tuloksena muodostetun gif-animaation."""
    gif_cmd = os.path.join("output", f"{map_name}_{scen_index}_{algorithm}.gif")
    if os.name != "nt":  # nt == Windows
        gif_cmd = "open " + gif_cmd
    os.system(gif_cmd)


def create_diagonal_path(start: tuple, end: tuple, path: set) -> set:
    """
    Lasketaan diagonaaliset xy-koordinaatit kahden solmun väliltä."""
    x1, y1 = start
    x2, y2 = end
    if x1 < x2 and y1 > y2:
        mod = (1, -1)
    elif x1 < x2 and y1 < y2:
        mod = (1, 1)
    elif x1 > x2 and y1 < y2:
        mod = (-1, 1)
    else:
        mod = (-1, -1)
    while (x1, y1) != end:
        x1, y1 = x1 + mod[0], y1 + mod[1]
        path.add((x1, y1))
    return path


def get_path_between_two_nodes(
    start: tuple, end: tuple, algorithm: str, visited: dict
) -> set:
    """Muodostaa ja palauttaa joukon solmuja kahden pisteen väliltä. Riippuen algoritmista,
    polun määritys myös eroaa. Funktio on tarkoitettu hyödynnettäväksi polun piirtämisessä
    kartan kuva-tiedostoon.

    Args:
        start (tuple): alkusolmu
        end (tuple): loppusolmu
        algorithm (str): Joko 'dijkstra', 'a_star' tai 'jps'.
        visited (dict): Sanakirja solmuja ja arvona tuple: (etäisyys, solmu mistä ollaan saavuttu)

    Returns:
        set: Joukko polun solmuja start ja end välillä.
    """
    path = {end}
    path_node = end
    if algorithm != "jps":
        while path_node != start:
            _, path_node = visited[path_node]
            path.add(path_node)
    else:
        while path_node != start:
            x1, y1 = path_node
            _, path_node = visited[path_node]
            x2, y2 = path_node
            # Solmut samalla rivillä
            if x1 == x2:
                for i in range(abs(y1 - y2)):
                    path.add((x1, min(y1, y2) + i))
            # Solmut samassa sarakkeessa
            elif y1 == y2:
                for i in range(abs(x1 - x2)):
                    path.add((min(x1, x2) + i, y1))
            # Solmujen väli on diagonaalinen
            else:
                path = create_diagonal_path((x1, y1), (x2, y2), path)
            path.add(path_node)
    return path


def form_base_img(map_name: str, dimensions: tuple):
    """Luo Image-olion assets-kansiosta löytyvälle kuvalle.

    Args:
        map_name (str): Kartan nimi.
        dimensions (tuple): Kuvan leveys ja korkeus.

    Returns:
        Image/None: Palautetaan PIL Image-olio,
        jos kartan nimellä löytyi .png tiedosto, muuten None.
    """
    try:
        im = Image.open(f"src/assets/images/{map_name}.png")
        return im.resize(dimensions, Image.Resampling.LANCZOS)
    except FileNotFoundError as ex:
        print(f"'{map_name}', {ex.strerror}")
        return None


def save_created_image(map_name: str, scen_index: int, algorithm: str, im: Image):
    im.save(f"output/{map_name}_{str(scen_index)}_{algorithm}.png", "PNG")


def calculate_circle_coords_around_origin(origin: tuple, radius: int) -> list:
    """Laskee ympyrän kehän koordinaatit.

    Args:
        origin (tuple): Ympyrän keskipiste.
        radius (int): Ympyrän säde.

    Returns:
        set: kokoelma ympyrän kehän pisteitä sekä sen keskipiste.
    """
    circle_coords = {origin}
    j, k = origin
    for t in range(360):
        x = floor(radius * cos(t) + j)
        y = floor(radius * sin(t) + k)
        if x < 0 or y < 0:
            continue
        circle_coords.add((x, y))
    return circle_coords


def draw_circles_around_start_and_goal(start: tuple, goal: tuple, im: Image) -> Image:
    """Värittää lähdön ja maalin ympäröimät pikselit niiden korostamiseksi.

    Args:
        start (tuple): Lähdön x,y-koordinaatit.
        goal (tuple): Maalin x,y-koordinaatit.
        im (Image): Kuva, johon pisteet korostetaan.

    Returns:
        Image: Kuva, johon maali- ja lähtöpisteet on korostettu.
    """
    pix = im.load()
    green = (0, 255, 0)
    red = (255, 0, 0)
    for origin, radius, color in (
        (start, 9, green),
        (start, 10, green),
        (goal, 9, red),
        (goal, 10, red),
    ):
        for coord in calculate_circle_coords_around_origin(origin, radius):
            try:
                pix[coord] = color
            except (
                IndexError
            ):  # Ympyrän kehä saattaa muodostua kuvan rajojen ulkopuolelle.
                pass
    return im


def draw_path_onto_map(
    path_start_and_end: tuple,
    goal: tuple,
    algorithm: str,
    nodes: dict,
    visited: dict,
    im: Image,
):
    """Piirtää karttaa edustavaan kuvaan löydetyn polun ja käsitellyt solmut.

    Args:
        path_start_and_end (tuple): Polun alun ja päätepisteen x,y -koordinaatit.
        goal (tuple): Etsittävä maali. Koordinaatteja käytetään korostamaan maalin
        sijaintia kartalla ympyröimällä se.
        algorithm (str): Algoritmin nimi, joko dijkstra, a_star tai jps.
        nodes (dict): Verkon solmut vieruslistana viimeistä kuvaa varten.
        visited (dict): sanakirja käsitellyistä solmuista. (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja viereinen koordinaatti mistä
    avain-koordinaattiin on kuljettu.
        im (PIL.Image): Kuva, jonka pikseleiden väriä muuttamalla
        polku sekä algoritmin käsittelemät solmut visualisoidaan.
    """
    pix = im.load()
    for node in visited:
        for _, n in nodes[node].items():
            if not n.obstacle and n.pruned:
                pix[n.coords] = (128, 128, 128)  # Karsitut solmut väri: (Harmaa)
        pix[node] = (0, 255, 255)  # Solmut missä käyty väri: (Cyan)
    im = draw_circles_around_start_and_goal(path_start_and_end[0], goal, im)
    path = get_path_between_two_nodes(
        path_start_and_end[0], path_start_and_end[1], algorithm, visited
    )
    for node in path:
        pix[node] = (255, 0, 255)  # Polku väri: (Magenta)
    return im


def draw_and_save_found_pathfinding(
    map_name: str,
    scen: dict,
    algorithm: str,
    nodes: dict,
    visited: dict,
):
    save_created_image(
        map_name,
        scen["index"],
        algorithm,
        draw_path_onto_map(
            (scen["start"], scen["goal"]),
            scen["goal"],
            algorithm,
            nodes,
            visited,
            form_base_img(map_name, (scen["dimensions"][0], scen["dimensions"][1])),
        ),
    )
