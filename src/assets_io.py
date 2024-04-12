import os
from pathlib import Path
import re
from PIL import Image
from graph import Graph


def __reader(file_path: str) -> list:
    """Apufunktio map ja scen tiedostojen lukemiseen.

    Args:
        file_path (str): polku luettavaan tiedostoon.

    Returns:
        list: lista tiedoston riveistä.
    """
    data = []
    try:
        with open(file_path, encoding="ascii") as file:
            return file.read().splitlines()
    except FileNotFoundError as ex:
        print(f"'{file_path}', {ex.strerror}")
    return data


def read_map(map_name: str) -> list:
    """Lukee ASCII map-tiedoston sisältö.

    Args:
        map_name (str): Tiedoston nimi ilman .map päätettä.

    Returns:
        list: Kaksiulotteinen lista ascii-merkkejä.
    """
    ascii_graph = []
    data = __reader(f"src/assets/maps/{map_name}.map")
    for row in data[4:]:
        ascii_graph.append(list(row))
    return ascii_graph


def read_scenarios(map_name: str) -> list:
    """Lukee scen-tiedoston skenaariot map tiedostolle.

    Args:
        map_name (str): Tiedoston nimi ilman .map.scen päätettä.

    Returns:
        list[dict]: Lista sanakirjoja skenaarioista. Nämä koostuvat:
        - start (tuple): lähdön x,y -koordinaatti
        - goal (tuple): maalin x,y -koordinaatti
        - shortest (int): lyhyin polku start ja goal välillä
        - dimensions (tuple): kartan leveys ja korkeus pikseleissä
    """
    scen_list = []
    data = __reader(f"src/assets/scens/{map_name}.map.scen")
    for row in data[1:]:
        scen = {}
        row = re.split(r"\s+", row)[::-1]
        scen["shortest"] = float(row[0])
        scen["goal"] = (int(row[2]), int(row[1]))
        scen["start"] = (int(row[4]), int(row[3]))
        scen["dimensions"] = (int(row[6]), int(row[5]))
        scen_list.append(scen)
    return scen_list


def create_diagonal_path(start: tuple, end: tuple, path: set) -> set:
    """
    Lasketaan diagonaaliset xy-koordinaatit kahden solmun väliltä."""
    x1, y1 = start
    x2, y2 = end
    if x1 < x2 and y1 > y2:
        mod = (1,-1)
    elif x1 < x2 and y1 < y2:
        mod = (1,1)
    elif x1 > x2 and y1 < y2:
        mod = (-1,1)
    else:
        mod = (-1,-1)
    while (x1,y1) != end:
        x1, y1 = x1+mod[0], y1 + mod[1]
        path.add((x1,y1))
    return path


def get_path_between_two_nodes(start: tuple, end: tuple, algorithm: str, visited: dict) -> set:
    """Muodostaa ja palauttaa joukon solmuja kahden pisteen väliltä. Riippuen algoritmista, 
    polun määritys myös eroaa.

    Args:
        start (tuple): alkusolmu
        end (tuple): loppusolmu
        algorithm (str): Joko 'dijkstra', 'A_star' tai 'jps'.
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
                for i in range(abs(y1-y2)):
                    path.add((x1,min(y1,y2)+i))
            # Solmut samassa sarakkeessa
            elif y1 == y2:
                for i in range(abs(x1-x2)):
                    path.add((min(x1,x2)+i,y1))
            # Solmujen väli on diagonaalinen
            else:
                path = create_diagonal_path((x1,y1),(x2,y2),path)
            path.add(path_node)
    return path


def draw_path_onto_map(map_name: str, scen_index: int, scen: dict, algorithm: str, graph: Graph):
    """Piirtää karttaa edustavaan kuvaan löydetyn polun ja käsitellyt solmut.
    Muokattu kuva tallennetaan output/ -kansioon

    Args:
        map_name (str): Tiedoston nimi ilman .png päätettä.
        scen_index (int): Erotteleva indeksi, joka lisätään kuvasta tallennettavan kopion nimeen.

        scen (dict): sanakirja skenaarion tiedoista. Tämä koostuu:
        - start (tuple): lähdön x,y -koordinaatti
        - goal (tuple): maalin x,y -koordinaatti
        - shortest (int): lyhyin polku start ja goal välillä
        - dimensions (tuple): kartan leveys ja korkeus pikseleissä

        visited (dict): sanakirja käsitellyistä solmuista. (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja viereinen koordinaatti mistä
    avain-koordinaattiin on kuljettu.
    """
    visited = graph.visited
    try:
        im = Image.open(f"src/assets/images/{map_name}.png")
        im = im.resize((scen["dimensions"][0], scen["dimensions"][1]), Image.Resampling.LANCZOS)
        pix = im.load()
        for node in visited:
            for _, n in graph.nodes[node].items():
                if not n.obstacle and n.pruned:
                    pix[n.coords] = (128,128,128)  # Karsitut solmut väri: (Harmaa)
            pix[node] = (0, 255, 255)  # Solmut missä käyty väri: (Cyan)

        path = get_path_between_two_nodes(scen["start"], scen["goal"], algorithm, visited)
        for node in path:
            pix[node] = (255, 0, 255)  # Polku väri: (Magenta)
        pix[scen["start"]] = (0, 255, 0)  # Alku väri: Vihreä
        pix[scen["goal"]] = (255, 0, 0)  # Maali väri: Punainen
        im.save(f"output/{map_name}_{str(scen_index)}_{algorithm}.png", "PNG")
    except FileNotFoundError as ex:
        print(f"'{map_name}', {ex.strerror}")


def get_available_maps():
    """Hakee listan saatavilla olevista kartoista,
    assets hakemiston png-tiedostojen perusteella.

    Returns:
        list: Lista tiedostojen nimiä, ilman tiedostopäätettä.
    """
    return [Path(filename).stem for filename in os.listdir("src/assets/images/")]
