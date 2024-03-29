# Viikkoraportti, viikko 3
Sain tällä viikolla kehitettyä ensimmäisen version JPS algoritmista. Määrittämieni testien perusteella algoritmin pitäisi toimia oikein, mutta en ole silti tyytyväinen sen tämänhetkiseen tehoon. En ole täysin varma kuinka tehokas sen pitäisi olla, mutta tällä hetkellä sillä on vaikeuksia voittaa Dijkstran algoritmia. Oletan, että kehittämäni karsimis-toiminnallisuus ei ole tarpeeksi tehokas ja tietorakenteeni eivät ole algoritmin funktioille optimaalisia. Myös polkujen laskeminen on epäoptimaalista, joten selvitän onko etäisyydet solmuista maaliin mahdollista esilaskea, ennen algoritmin toimintaa.

Toisaalta, jos olen oikein ymmärtänyt, mitä enemmän esteitä verkossa, sitä enemmän hyppypisteitä algoritmi muodostaa. JPS näyttäisikin toimivan selkeästi parhaiten avoimissa kartoissa, missä Dijkstralla on enemmän käsiteltäviä solmuja.

## Tuntikirjanpito

| Päivä | Käytetty aika | Kuvaus |
| ----- | ------------- | ------ |
| 25.3.  | 5h | Aloitettu JPS algoritmin kehitys ja päivitetty verkko-luokkaa |
| 26.3.  | 2,5h | Kehitetty JPS algoritmille naapureiden karsimis-funktio ja tälle testit  |
| 26.3.  | 2,25h | Kehitetty JPS algoritmille jump point solmujen haku ja kokoamis funktiot ja näille testit  |
| 27.3.  | 5,75h | Kehitetty loppu toiminnallisuus JPS algoritmista, lisätty testejä ja algoritmin suoritus pääohjelmaan  |
| 29.3.  | 1,5h | Päivitetty dokumentaatiota  |
| Total  | 17h |  |
