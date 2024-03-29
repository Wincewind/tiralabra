# Algoritmit ja tekoäly -harjoitustyö: polunetsintä algoritmien vertailua
[![GHA workflow badge](https://github.com/Wincewind/tiralabra/workflows/CI/badge.svg)](https://github.com/Wincewind/tiralabra/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Wincewind/tiralabra/graph/badge.svg?token=TGY0XJ0UZM)](https://codecov.io/gh/Wincewind/tiralabra)

## Dokumentaatio
- [Määrittelydokumentti](dokumentaatio/Määrittelydokumentti.md)
- [Testausdokumentti](dokumentaatio/Testausdokumentti.md)

### Viikkoraportit
- [Viikkoraportti 1](dokumentaatio/viikkoraportit/viikkoraportti_1.md)
- [Viikkoraportti 2](dokumentaatio/viikkoraportit/viikkoraportti_2.md)
- [Viikkoraportti 3](dokumentaatio/viikkoraportit/viikkoraportti_3.md)

## Asennus
1. Kun repo on kloonattu haluamaasi hakemistoon, siirry projektin juurihakemistoon ja asenna riippuvuudet komennolla:
```bash
poetry install
```
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
poetry run coverage html
```
tai erillinen html-tiedosto:
```bash
poetry run coverage report -m
```
Raportti generoituu _htmlcov/_-hakemistoon.

### Pääohjelman käynnistäminen
Pääohjelman käynnistys tapahtuu suorittamalla komento:

```bash
poetry run python src\main.py
```
Jos ohjelma halutaan keskeyttää ennenaikaisesti, tapahtuu tämä syöttämällä komentokehotteeseen näppäinyhdistelmä _CTRL+C_ .

### Pylint

Laatutarkistuksen pytyy suorittamaan [.pylintrc](.pylintrc) määritysten mukaisesti komennolla:

```bash
poetry run pylint src
```
