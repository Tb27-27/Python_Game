https://www.pygame.org/project/5291/7669
https://www.youtube.com/watch?v=37phHwLtaFg
https://thorbjorn.itch.io/tiled
https://szadiart.itch.io/rogue-fantasy-catacombs
https://cainos.itch.io/pixel-art-top-down-basic


---

# Map documentation

Ik heb opgezocht wat voor opties er zijn voor maps, ik ga een tile systeem gebruiken met vrije movement van de speler en enemies.


Hoe ga ik de map maken?
3 lagen
* Achtergrond
* Collision Layer
* Voorgrond (obstacels/objecten)

De Achtergrond maak ik eerst met de hulp van tiled, een programma waar je makkelijk tilemaps kan maken en exporteren.
De collision layer gaat daar boven, dus waar enemies en de player niet door heen kunnen met hulp van een array.
Daarboven doe ik de voorgrond layer, sprites waar de speler achter kan staan.