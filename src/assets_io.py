import re
from PIL import Image


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
    """
    scen_list = []
    data = __reader(f"src/assets/scens/{map_name}.map.scen")
    for row in data[1:]:
        scen = {}
        row = re.split(r"\s+", row)[::-1]
        scen["shortest"] = float(row[0])
        scen["goal"] = (int(row[2]), int(row[1]))
        scen["start"] = (int(row[4]), int(row[3]))
        scen_list.append(scen)
    return scen_list


def draw_path_onto_map(map_name: str, scen_index: int, scen: dict, visited: dict):
    """Piirtää karttaa edustavaan kuvaan löydetyn polun ja käsitellyt solmut.
    Muokattu kuva tallennetaan /src/output/ -kansioon

    Args:
        map_name (str): Tiedoston nimi ilman .png päätettä.
        scen_index (int): Erotteleva indeksi, joka lisätään kuvasta tallennettavan kopion nimeen.

        scen (dict): sanakirja skenaarion tiedoista. Tämä koostuu:
        - start (tuple): lähdön x,y -koordinaatti
        - goal (tuple): maalin x,y -koordinaatti
        - shortest (int): lyhyin polku start ja goal välillä

        visited (dict): sanakirja käsitellyistä solmuista. (x,y)-koordinaatti on avain ja arvona
    on tuple muodossa koordinaattiin kuljettu lyhyin matka ja viereinen koordinaatti mistä
    avain-koordinaattiin on kuljettu.
    """
    try:
        im = Image.open(f"src/assets/images/{map_name}.png")
        im = im.resize((512, 512), Image.Resampling.LANCZOS)
        pix = im.load()
        for node in visited:
            pix[node] = (0, 255, 255)  # Solmut missä käyty väri: (Cyan)

        _, path_node = visited[scen["goal"]]
        while path_node != scen["start"]:
            pix[path_node] = (255, 0, 255)  # Polku väri: Magenta
            _, path_node = visited[path_node]
        pix[scen["start"]] = (0, 255, 0)  # Alku väri: Vihreä
        pix[scen["goal"]] = (255, 0, 0)  # Maali väri: Punainen
        im.save(f"src/output/{map_name}_{str(scen_index)}.png", "PNG")
    except FileNotFoundError as ex:
        print(f"'{map_name}', {ex.strerror}")