# Määrittelydokumentti
Opinto-ohjelma: Tietojenkäsittelytieteen kandidaatti (TKT)

## Projektin aihe
Tavoitteena on toteuttaa 2-3 polunetsintä algoritmia ja vertailla niiden nopeuksia hyödyntäen [Moving AI Labin](https://www.movingai.com/benchmarks/) 2D pikselikarttoja ja skenaarioita. Vertailua on tarkoitus tehdä ainakin Dijkstran ja JPS algoritmeilla, mutta koska JPS on optimoitu versio A*:sta, pyritään myös A* sellaisenaan sisällyttämään vertailuun. Polunetsintään kuluvan ajan mittauksen lisäksi piirretään karttaan löydetty polku ja käsitellyt solmut etsinnässä, jota voidaan hyödyntää testauksessa ja algoritmien oikeellisuuden toteamisessa. Jos sille riittää aikaa, yritetään projektissa myös toteuttaa ajan mittauksesta erillinen animaatio polkujen muodostamiselle. Algoritmien toimintaa saatetaan yrittää visualisoida myös samanaikaisesti hyödyntäen säikeitä. 

Käyttäjä voisi valita manuaalisesti vertailussa käytettäviä karttoja ja skenaarioita tai ohjelman voi antaa valita näistä satunnainen tapaus.

## Toteutettavat algoritmit
-  Dijkstran algoritmi: [Wikipedia, Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
-  A*-algoritmi: [Wikipedia, A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
-  JPS: [Harabor, D. and Grastien, A. 2011. Online Graph Pruning for Pathfinding On Grid Maps. Proceedings of the AAAI Conference on Artificial Intelligence. 25, 1 (Aug. 2011)](https://doi.org/10.1609/aaai.v25i1.7994)

## Ohjelmointi kieli
Ohjelmoinnissa käytettävä kieli on Python. Minulla on myös jonkun verran kokemusta C# ja VB.NET ohjelmoinnista ja uskon kykeneväni vertaisarvioimaan näillä kielillä toteutettuja projekteja. 

## Dokumentaatio
Dokumentaatio ja koodin kommentit kirjoitetaan suomeksi, mutta esim. funktioiden ja muuttujien nimet ovat englanniksi.
