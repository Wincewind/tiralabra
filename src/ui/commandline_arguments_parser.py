from argparse import ArgumentParser
from assets_io import get_available_maps

parser = ArgumentParser()
parser.add_argument('-m', '--map', default='',
                    help=f'Kartan nimi, jolle testit ajetaan. \
                        Valittavana on: {", ".join(get_available_maps())}',
                        type=str, dest='map_name',choices=get_available_maps())
parser.add_argument("-t", "--test", help="Testin tyyppi, 1: ajetaan vain yksi skenaario, \
                    2: ajetaan x määrä satunnaisia skenaarioita",
                    type=int, choices=[1, 2], dest='test_type',default=-1)
parser.add_argument("-s", "--scenarios", help="Ajettavien skenaarioiden indeksit, jos test_type=1. \
                    Huom. eri kartoilla on eri määrä ajettavia skenaarioita",
                    type=int, dest='scenario', nargs="+", default=-1)
parser.add_argument("-c", "--count", help="Satunnaisten skenaarioiden lukumäärä, jos test_type=2",
                    type=int, dest='amount', default=-1)
parser.add_argument("-i", "--images", help="Valinnalla voidaan estää pääohjelmaa piirtämästä kuvia \
                    algoritmien testeistä. Oletuksena kuvat piirretään.",
                    dest='images', default=True, action="store_false")
parser.add_argument("-a", "--algorithms", help="Valinnalla voidaan valita, \
                    mitä algoritmeja halutaan testata.",
                    dest='algorithms', choices=["dijkstra","A_star","jps"],
                    nargs="+", default=["dijkstra","A_star","jps"])
