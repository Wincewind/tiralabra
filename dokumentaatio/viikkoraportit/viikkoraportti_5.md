# Viikkoraportti, viikko 5

Testasin vieruslistojen vaihtamista listoiksi sanakirjojen sijaan ja tämä näytti nopeuttavan algoritmeja n. 30 %. Koska tämä ei näyttänyt varsinaisesti kasvattavan eroa eri algoritmien nopeuksien välillä ja muutos vaatisi myös mittavia testien päivityksiä, en taida toteuttaa muutosta.

Ensi viikolla ajattelin hienosäätää visualisointia esim. nostamalla esiin kuvissa lähtö- ja maalipisteitä paremmin ja lisäämällä satunnaiseen karttavalintaan min-max valinnan. GIF-animaatiot olisi hyödyllistä saada käyttäjälle automaattisesti avattua, mutta tähän ei ole toistaiseksi löytynyt kätevää Python kirjastoa, kuten `matplotlib` kuvilla. 

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 15.4.  | 1h | Yritetty tehostaa JPS algoritmia |
| 16.4.  | 3,5h | Testattu vieruslistojen vaihtamista yksiulotteisiksi |
| 16.4.  | 3,5h | Lisätty GIF-animaation generointi optio |
| 18.4.  | 1,5h | Refaktoroitu koodia ja täydennetty testikattavuutta |
| 19.4.  | 2h | Vertaisarvio ja päivitetty dokumentaatiota |
| Total  | 11,5h |  |
