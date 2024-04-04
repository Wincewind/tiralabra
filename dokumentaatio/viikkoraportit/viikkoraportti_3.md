# Viikkoraportti, viikko 3
Sain tällä viikolla kehitettyä ensimmäisen version JPS algoritmista. Määrittämieni testien perusteella algoritmin pitäisi toimia oikein, mutta en ole silti tyytyväinen sen tämänhetkiseen tehoon. En ole täysin varma kuinka tehokas sen pitäisi olla, mutta tällä hetkellä sillä on vaikeuksia voittaa Dijkstran algoritmia. Oletan, että kehittämäni karsimis-toiminnallisuus ei ole tarpeeksi tehokas ja tietorakenteeni eivät ole algoritmin funktioille optimaalisia. Myös polkujen laskeminen on epäoptimaalista, joten selvitän onko etäisyydet solmuista maaliin mahdollista esilaskea, ennen algoritmin toimintaa.

Toisaalta, jos olen oikein ymmärtänyt, mitä enemmän esteitä verkossa, sitä enemmän hyppypisteitä algoritmi muodostaa. JPS näyttäisikin toimivan selkeästi parhaiten avoimissa kartoissa, missä Dijkstralla on enemmän käsiteltäviä solmuja.

Lisäsin projektiin A* algoritmin, jotta JPS:iä voidaan vertailla myös tähän. Muokkasin hieman etäisyyksien laskentaa, joka nopeutti A* ja JPS:iä. JPS ja A* ovat selvästi Dijkstraa nopeampia näille otollisissa kartoissa, kuten kaupunkikartat, mutta JPS on lähes kaikilla reitellä A*:ia hitaampi.

#### Päivitys 4.4.
Sain viimein nopeutettua JPS:ää erottelemalla pakotettujen naapureiden tarkistuksen ja karsimisen, niin että karsimista tarvitsee suorittaa vain seuraavaa hyppypistettä tarkastellessa (kuten JPS julkaisun algoritmissa 1 on kuvattu). Nyt JPS:ltä menee puolet vähemmän aikaa polunetsintään ja se näyttäisi omassa kehitysympäristössäni häviävän Dijkstralle ja A*:lle ainoastaan todella tiheissä sokkeloissa.

Ajattelin yrittää ensi viikolla lisätä pääohjelmaan mahdollisuuden ajaa sitä komentoriviargumenteilla, jolloin ajoja voi suorittaa ilman että syötteitä tarvitsee kirjoittaa joka kerta uudestaan. Tällä voisi vaikuttaa myös esim. ajetaanko skenaarioita kaikilla vai vaan 1-2 algoritmilla. Myös reitin piirtämisen deaktivointi voisi olla mahdollista.

Tarkempien mittaustulosten takaamiseksi ajattelin myös, että algoritmit suoritetaan useampaan kertaan ja käytetään vertailussa näiden keskiarvoja.

## Tuntikirjanpito

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 25.3.  | 5h | Aloitettu JPS algoritmin kehitys ja päivitetty verkko-luokkaa |
| 26.3.  | 2,5h | Kehitetty JPS algoritmille naapureiden karsimis-funktio ja tälle testit  |
| 26.3.  | 2,25h | Kehitetty JPS algoritmille jump point solmujen haku ja kokoamis funktiot ja näille testit  |
| 27.3.  | 5,75h | Kehitetty loppu toiminnallisuus JPS algoritmista, lisätty testejä ja algoritmin suoritus pääohjelmaan  |
| 29.3.  | 1,5h | Päivitetty dokumentaatiota  |
| 2.4.  | 2h | Yritetty hienosäätää JPS algoritmia, kehitetty A* algoritmia  |
| 3.4.  | 2h | Yritetty hienosäätää JPS algoritmia, kehitetty A* algoritmia ja päivitetty dokumentaatiota  |
| 4.4.  | 3h | Refaktoroitu JPS algoritmia ja kommentoitu koodia  |
| Total  | 24h |  |
