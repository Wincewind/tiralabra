from argparse import ArgumentParser
from services.assets_service import get_available_maps

parser = ArgumentParser()
parser.add_argument(
    "-m",
    "--map",
    default="",
    help="Kartan nimi, jolle testit ajetaan.",
    type=str,
    dest="map_name",
    choices=get_available_maps(),
)
parser.add_argument(
    "-t",
    "--test",
    help="Testin tyyppi, 1: ajetaan vain tietty(jä) skenaario(ita), \
                    2: ajetaan x määrä satunnaisia skenaarioita",
    type=int,
    choices=[1, 2],
    dest="test_type",
    default=-1,
)
parser.add_argument(
    "-s",
    "--scenarios",
    help="Ajettavien skenaarioiden indeksit, jos test_type=1. \
                    Huom. eri kartoilla on eri määrä ajettavia skenaarioita",
    type=int,
    dest="scenario",
    nargs="+",
    default=None,
)
parser.add_argument(
    "-c",
    "--count",
    help="Satunnaisten skenaarioiden lukumäärä, jos test_type=2",
    type=int,
    dest="amount",
    default=-1,
)
parser.add_argument(
    "-i",
    "--images",
    help="Valinnalla voidaan estää pääohjelmaa piirtämästä kuvia \
                    algoritmien testeistä. Oletuksena kuvat piirretään",
    dest="images",
    default=True,
    action="store_false",
)
parser.add_argument(
    "-a",
    "--algorithms",
    help="Valinnalla voidaan valita, \
                    mitä algoritmeja halutaan testata",
    dest="algorithms",
    choices=["dijkstra", "a_star", "jps"],
    nargs="+",
    default=["dijkstra", "a_star", "jps"],
)
parser.add_argument(
    "-p",
    "--path",
    help="Löydetyn polun pituus tulostetaan",
    dest="print_path_len",
    default=False,
    action="store_true",
)
parser.add_argument(
    "--allow_corner_cuts",
    help="Oletuksena esteiden kulmien leikkausta ei sallita. \
                    Tällä argumentilla voidaan se mahdollistaa, jolloin löydetyt polut ovat lyhyempiä.",
    dest="no_corner_cuts",
    default=True,
    action="store_false",
)

parser.add_argument(
    "-g",
    "--gif",
    help="Muodosta polunetsinnästä gif-animaatio.",
    dest="gif",
    default=False,
    action="store_true",
)