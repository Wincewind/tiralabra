# Toteutusdokumentti 
Työssä ei ole käytetty laajoja kielimalleja. 

## Ohjelman yleisrakenne 
Ohjelma koostuu neljästä eri osasta: 

### Käyttäjäsyötteiden käsittely 
Ohjelman voi käynnistää joko normaalisti tai hyödyntäen [komentorivi-argumentteja](https://github.com/Wincewind/tiralabra/blob/main/README.md#p%C3%A4%C3%A4ohjelman-k%C3%A4ynnist%C3%A4minen-komentorivi-argumenteilla). Käyttäjän syötteiden tuloksena valitaan jokin /assets/-kansion kartoista, sen skenaariot ja aloitetaan polunetsintä algoritmeilla. 

### Karttatiedostojen käsittely 
Verkko, mihin polunetsintä suoritetaan, muodostetaan .map tiedostoista, missä on ASCII-merkeillä esitetty karttojen kuvia vastaavat pikselit. Merkit luetaan ja jaotellaan kaksiulotteiseen listaan verkon muodostamista varten. Tulosten esittämistä varten, hyödynnetään Pythonin PIL-kirjastoa värittämään polun, lähtö, maali ja karsittujen solmujen pikseleitä tietyillä väreillä. 

### Verkkotietorakenne ja sen muodostus 
Ohjelman tietorakenteet on toteutettu luokkana, jossa on sanakirjat verkolle sekä etäisyyksille, mihin kirjataan myös polun aiemmat solmut, jotta polku voidaan jälkikäteen piirtää. Verkko on vieruslista, missä naapurit on numeroitu niiden suunnan mukaan 0-7. Numerointi alkaa kohtisuoraan ylhäältä nollalla ja sitä jatketaan myötäpäivään. Suuntaa hyödynnetään JPS algoritmissa, koska riippuen siitä saattaa esimerkiksi hyppypisteiden haku erota. Jos kulman leikkaus, eli esteen vierestä kulkeminen diagonaalisesti halutaan kieltää, on tähän asetus, joka poistaa kyseiset naapurit solmuilta. Solmuilla on myös oma luokkansa vieruslistassa, joihin voi JPS algoritmi merkitä, että kyseinen naapurisolmu on karsittu. 

### Algoritmien suoritus 
Kun karttojen tiedot on luettu ja verkko muodostettu, otetaan karttojen skenaario tiedoista etsittävälle polulle alku ja loppu koordinaatit. Nämä verkko-olion lisäksi ovat algoritmeilla ainoat tarvittavat syötteet, jonka jälkeen polunetsintää voidaan suorittaa Dijkstra, A* ja JPS algoritmeilla. Pääasiallinen suoritettava vertailu ohjelmassa on algoritmien suoritusajat. Algoritmeja ajetaan muutama kerta ja ohjelma tulostaa mittausten keskiarvon. Jos kuvien muodostus on käytössä, ohjelma avaa näytölle kuvan muodostetusta polusta jokaisella ajettavalla algoritmilla. 

Kun kaikki valitut skenaariot on ajettu tulostaa ohjelma komentokehotteeseen jokaisen algoritmin polunetsinnän kestojen keskiarvojen summan.  

## Aikavaativuudet 

n solmun verkossa, missä on m kaarta, täytyy Dijkstran algoritmin käydä pahimmassa tapauksessa kaikki läpi ajassa O(n + m). Jokainen kaari lisätään binäärikekoon niiden löytyessä ja poistetaan sieltä, kun se käsitellään, jossa kummassakin kestää O(m log m). Tällöin aikavaativuus on siis O(n + m log m). 

A* heuristiikasta riippuen, sen aikavaativuus on pahimmassa tapauksessa keskimääräinen määrä solmujen naapureita b, lyhyimmän polun pituuden d potenssiin: O(b^d). Sama pätee sen tilavaativuutta. 

JPS jakaa aikavaativuutensa A* kanssa, mutta siinä missä A* käyttää n. 50-50 ajastaan naapureiden läpikäymisessä ja keon käsittelyssä, JPS tavoitteena on vähentää huomattavasti kekoon lisättäviä alkioita ja keskittyy suurimmanosan suorituksesta oleellisten hyppypisteiden etsimiseen, jolloin käytetty aikajakauma on n. 90-10. 

## Työn mahdolliset puutteet ja parannusehdotukset 

Tämänhetkisessä toteutuksessa etenkin tietorakenteiden parantaminen olisi mahdollista. Vieruslistan voisi esimerkiksi implementoida listana sanakirjan sijasta ja määrittää solmuille listan indeksejä vastaavat luvut. JPS algoritmista on myös uudempia variaatioita, joilla on yritetty täydentää alkuperäisen version heikkouksia. 

## Lähteet 

[A. Laaksonen: Tietorakenteet ja algoritmit](https://www.cs.helsinki.fi/u/ahslaaks/tirakirja/) 

[Wikipedia: Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) 

[Wikipedia: A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) 

[AAAI, Harabor, D. and Grastien, A: Online Graph Pruning for Pathfinding On Grid Maps](https://doi.org/10.1609/aaai.v25i1.7994) 

[AAAI, Harabor, D. and Grastien, A: Improving Jump Point Search](https://doi.org/10.1609/icaps.v24i1.13633) 
