import os
from pathlib import Path
import re
from random import choices


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
    for i,row in enumerate(data[1:]):
        scen = {}
        row = re.split(r"\s+", row)[::-1]
        scen["index"] = i
        scen["shortest"] = float(row[0])
        scen["goal"] = (int(row[2]), int(row[1]))
        scen["start"] = (int(row[4]), int(row[3]))
        scen["dimensions"] = (int(row[6]), int(row[5]))
        scen_list.append(scen)
    return scen_list


def get_available_maps():
    """Hakee listan saatavilla olevista kartoista,
    assets hakemiston png-tiedostojen perusteella.

    Returns:
        list: Lista tiedostojen nimiä, ilman tiedostopäätettä.
    """
    return [Path(filename).stem for filename in os.listdir("src/assets/images/")]


def get_random_scens(scens:list, amount:int, shortest_range: list):
    if len(shortest_range) < 2:
        shortest_range.append(float("inf"))
    scens = [scen for scen in scens if shortest_range[0] <= scen["shortest"] <= shortest_range[1]]
    if len(scens) < amount:
        print(f"Lyhimmän polun pituusväliltä {shortest_range[0]} - {shortest_range[1]} \
löytyy vain {len(scens)} skenaariota.")
        amount = len(scens)
    return choices(scens, k=int(amount))
