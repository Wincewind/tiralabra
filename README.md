# Algoritmit ja tekoäly -harjoitustyö: polunetsintä algoritmien vertailua
[![GHA workflow badge](https://github.com/Wincewind/tiralabra/workflows/CI/badge.svg)](https://github.com/Wincewind/tiralabra/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Wincewind/tiralabra/graph/badge.svg?token=TGY0XJ0UZM)](https://codecov.io/gh/Wincewind/tiralabra)

## Dokumentaatio
- [Määrittelydokumentti](dokumentaatio/Määrittelydokumentti.md)
- [Testausdokumentti](dokumentaatio/Testausdokumentti.md)
- [Toteutusdokumentti](dokumentaatio/Toteutusdokumentti.md)

### Viikkoraportit
- [Viikkoraportti 1](dokumentaatio/viikkoraportit/viikkoraportti_1.md)
- [Viikkoraportti 2](dokumentaatio/viikkoraportit/viikkoraportti_2.md)
- [Viikkoraportti 3](dokumentaatio/viikkoraportit/viikkoraportti_3.md)
- [Viikkoraportti 4](dokumentaatio/viikkoraportit/viikkoraportti_4.md)
- [Viikkoraportti 5](dokumentaatio/viikkoraportit/viikkoraportti_5.md)
- [Viikkoraportti 6](dokumentaatio/viikkoraportit/viikkoraportti_6.md)

## Asennus
Kun repo on kloonattu haluamaasi hakemistoon, siirry projektin juurihakemistoon ja asenna riippuvuudet komennolla:
```bash
poetry install
```
Virtuaaliympäristön voi aktivoida komennolla:
```bash
poetry shell
```
mutta komennot suoritetaan myös virtuaaliympäristössä kun ne aloitetaan _poetry run_:lla.

## Komentorivitoiminnot

### Testaus
Testit voidaan suorittaa komennolla:
```bash
poetry run pytest src
```

### Testikattavuus
Testikattavuusraportin voi generoida komennoilla:
```bash
poetry run coverage run --branch -m pytest src
```
ja tuloksista saadaan yleiskatsaus komentoriville komennolla:
```bash
poetry run coverage report -m
```
tai erillinen html-tiedosto:
```bash
poetry run coverage html
```
Raportti generoituu _htmlcov/_-hakemistoon.

### Pääohjelman käynnistäminen
Pääohjelman käynnistys tapahtuu suorittamalla komento:

```bash
poetry run python src/main.py
```
Jos ohjelma halutaan keskeyttää ennenaikaisesti, tapahtuu tämä syöttämällä komentokehotteeseen näppäinyhdistelmä `CTRL+C` .

### Pääohjelman käynnistäminen komentorivi-argumenteilla
Pääohjelman voi käynnistää myös käyttäen komentorivi-argumentteja. Näillä säätämällä voi testausta kustomoida itsellensä sopivaksi ja saatavilla on myös enemmän optioita. Suoritusaikojen keskiarvojen lisäksi, voidaan myös esim. tulostaa odotettu ja löydetty polun pituus, ajaa vain tiettyjä algoritmeja tai ottaa pois käytöstä reitin piirtämisen ja kuvan tuottamisen. Kun halutaan suorittaa jokin testiajo uudestaan on näiden käytöstä erityisesti hyötyä. Suorittamalla komennon:
```bash
poetry run python src/main.py -h
```
Pitäisi näkyä seuraavat ohjeet:
```bash
usage: main.py [-h] [-m {64room_001,AR0406SR,AR0413SR,London_1_512,maze512-16-0}] [-t {1,2}] [-s SCENARIO [SCENARIO ...]] [-c AMOUNT] [-r [SHORTEST_RANGE ...]] [-i]
               [-a {dijkstra,a_star,jps} [{dijkstra,a_star,jps} ...]] [-p] [--allow_corner_cuts] [-g]

options:
  -h, --help            show this help message and exit
  -m {64room_001,AR0406SR,AR0413SR,London_1_512,maze512-16-0}, --map {64room_001,AR0406SR,AR0413SR,London_1_512,maze512-16-0}
                        Kartan nimi, jolle testit ajetaan.
  -t {1,2}, --test {1,2}
                        Testin tyyppi, 1: ajetaan vain tietty(jä) skenaario(ita), 2: ajetaan x määrä satunnaisia skenaarioita
  -s SCENARIO [SCENARIO ...], --scenarios SCENARIO [SCENARIO ...]
                        Ajettavien skenaarioiden indeksit, jos test_type=1. Huom. eri kartoilla on eri määrä ajettavia skenaarioita
  -c AMOUNT, --count AMOUNT
                        Satunnaisten skenaarioiden lukumäärä, jos test_type=2
  -r [SHORTEST_RANGE ...], --range [SHORTEST_RANGE ...]
                        Määrittää satunnaisille skenaarioille lyhimmän polun ala- ja/tai ylärajan, jos test_type=2. Arvoksi voi antaa joko vain alarajan tai ala- ja ylärajan. Arvoja voi syöttää enemmän kuin kaksi, mutta vain kaksi ensimmäistä otetaan huomioon.
  -i, --images          Valinnalla voidaan estää pääohjelmaa piirtämästä kuvia algoritmien testeistä. Oletuksena kuvat piirretään
  -a {dijkstra,a_star,jps} [{dijkstra,a_star,jps} ...], --algorithms {dijkstra,a_star,jps} [{dijkstra,a_star,jps} ...]
                        Valinnalla voidaan valita, mitä algoritmeja halutaan testata
  -p, --path            Löydetyn polun pituus tulostetaan
  --allow_corner_cuts   Oletuksena esteiden kulmien leikkausta ei sallita. Tällä argumentilla voidaan se mahdollistaa, jolloin löydetyt polut ovat lyhyempiä.
  -g, --gif             Muodosta polunetsinnästä gif-animaatio.
```
**Huom #1!**, argumentilla -c ei ole mitään ylärajaa, joten suorituksessa voi kestää todella kauan jos se on paljon kymmentä korkeampi. Keskeyttäminen tapahtui näppäinyhdistelmällä `CTRL+C` .

**Huom #2!**, gif-animaatiota ei tällä hetkellä pystytä näyttämään käyttäjälle ajon päätteeksi, mutta muodostetut animaatiot löytyvät `output`-kansiosta nimellä:
`{kartan nimi}_{suoritetun skenaarion indeksi}_{algoritmi jonka suorituksesta animaatio luotu, dijkstra/A_star/jps}.gif`

Komentorivi-argumentteja voi käyttää esim. seuraavasti:
```bash
poetry run python src/main.py -m London_1_512 -t 1 -s 100 200 300 -p
```
jonka seurauksena ajetaan kartalla London_1_512 skenaariot 100, 200 ja 300 niin että ajanmittauksen lisäksi tulostetaan skenaariolle algoritmin löytämän polun pituus.

Komennolla:
```bash
poetry run python src/main.py -m maze512-16-0 -t 2 -c 20 -a a_star jps -i -r 100
```
suoritetaan kartalla maze512-16-0 polunetsintä ainoastaan A* ja JPS algoritmeilla 20:ssä satunnaisessa skenaariossa, joiden lyhimmän reitin pituus on pidempi kuin 100. Kuvia löydetystä polusta ei muodosteta. **Huom!** tämän suorittamisessa saattaa kestää hetki.

Komennolla:
```bash
poetry run python src/main.py -m 64room_001 -t 2 -c 5 -a a_star jps -i -g -r 600 700
```
suoritetaan kartalla 64room_001 polunetsintä ainoastaan A* ja JPS algoritmeilla viidessä satunnaisessa skenaariossa, joiden lyhimmän reitin pituus on välillä 600-700. Kuvia löydetystä polusta ei muodosteta, mutta gif-animaatiot muodostetaan. **Huom!** GIF-animaatioiden muodostaminen pidentää polunetsintään kuluvaa aikaa. Mitä pidempi etsittävä reitti, sitä pidempi on myös animaatio. 

### Pylint

Laatutarkistuksen pytyy suorittamaan [.pylintrc](.pylintrc) määritysten mukaisesti komennolla:

```bash
poetry run pylint src
```
