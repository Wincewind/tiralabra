# Testausdokumentti

## Mitä on testattu
Ohjelmistossa on neljä testauksen kohdetta: algoritmit, tietorakenteet, syötteiden käsittely ja pääohjelma. Testit on tehty käyttäen Unittest-kehystä ja testit suorittavat yksikkötestausta yksittäisille toiminnoille, integraatio testausta kokonaisuuksille ja pääohjelman tapauksessa päästä päähän -testausta. Repositoriossa on käytössä GitHub actions, jolla nämä testit ajetaan pilvi-ympäristössä aina kun src-hakemistoa muokataan. Testauksen ulkopuolelle on jätetty käyttöliittymä, joka tässä tapauksessa on ainoastaan komentorivi syötteiden luku ja tulostus pääohjelmassa.

## Testikattavuus
![testikattavuus_vko3](viikkoraportit/testikattavuus_vko3.png)

## Testisyötteet
JPS algoritmin funktioiden testaamisessa on käytetty syötteinä julkaisussa esitettyjä tilanteita, jotka määrittävät algoritmin naapureiden karsimissääntöjä, pakotettuja naapureita ja hyppypisteitä. Näillä on yleensä jokin määriteltävä lukumäärä, johon algoritmin tulosta voidaan verrata. Polunetsinnän tulosten varmistamisessa on määritetty pieniä verkkoja, joille on lyhyin polku pystytty laskemaan käsin. Algoritmien toteutusten oikeellisuutta on myös testattu vertaamalla niitten tuloksia toisiinsa. Verkon muodostuksessa, syötteiden käsittelyssä ja näiden integraatiotestauksessa hyödynnetään Moving AI Labin karttoja ja skenaarioita. Näitä on myös hyödynnetty algoritmien laajemmassa testauksessa, missä algoritmin löytämän polun pituutta verrataan skenaariossa määritettyyn. Pidemmillä poluilla tulee kuitenkin huomattava määrä pyöristyseroa odotetun tuloksen ja algoritmin välillä, joten näitä testejä suoritetaan rajallinen määrä.

## Testien suorittaminen
Testejä voidaan suorittaa lokaalisti ja näistä testikattavuus raportin voi generoida [README.md ohjeiden](https://github.com/Wincewind/tiralabra?tab=readme-ov-file#testikattavuus) avulla.
