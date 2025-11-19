## Voorblad

### Naam:
Tom Bijsterbosch

### Klas:
OITSDO24A

### Studentennummer:
2220046

### Projectnaam:
Pythy

---

## Inleiding: 

### Hoe heet je project

Pythy

### Wat doet je applicatie

Het is een survival horror game die plaats vind in een cathedraal. Je probeert deze plek te ontsnappen, omdat je niet alleen bent.

### Waarom heb je voor dit idee gekozen? 

Ik hou heel erg van survival horror spellen, en ook heel erg van indie games.
Recent zijn mijn favoriete in dit genre:
"Signalis" en "Fear and Hunger"

Maar ik werd verliefd met het genre door oudere games zoals:
Clock Tower, Silent Hill, Resident Evil

Het lijkt me leuk om te kijken hoe een spel in python gemaakt kan worden in python met bijvoorbeeld .

### Wat is het hoofddoel van je project?

Een atmospherisch spel te maken.

---

## Functionaliteit: 

```
Beschrijf ten minste vijf functies uit je programma. 
Vermeld ook per functie wat de gebruiker ermee kan doen.

```

### Vijf Kernfuncties:

#### 1. Player Movement & Collision System
**Wat de gebruiker kan doen:**
De speler kan met de pijltjestoetsen of WASD door de cathedraal bewegen. Het collision-systeem voorkomt dat de speler door muren loopt en detecteert interacties met objecten en vijanden.

#### 2. Dynamic Light System met Fog-of-War
**Wat de gebruiker kan doen:**
De speler heeft een beperkte lichtcirkel om zich heen in de donkere cathedraal. Alleen het gebied binnen deze cirkel is zichtbaar, de rest blijft verborgen in duisternis. Dit zorgt voor spanning en beperkt het zicht.

#### 3. Enemy AI met Pathfinding
**Wat de gebruiker kan doen:**
De speler moet vijanden ontwijken of confronteren. Vijanden patrouilleren door de cathedraal en jagen de speler wanneer deze in zicht komt. De speler moet tactisch bewegen om te overleven.

#### 4. Inventory & Interaction System
**Wat de gebruiker kan doen:**
De speler kan items oppakken zoals sleutels, medicijnen en wapens. Met de "e" toets of "spatie" toets kan de speler interacten met objecten zoals deuren, kisten en puzzel-elementen. Items in de inventory kunnen gebruikt worden om verder te komen.


#### 5. Health & Damage System
**Wat de gebruiker kan doen:**
De speler heeft een health bar/hartslag die zichtbaar is in de UI. Bij contact met vijanden verliest de speler health. 
Door medicijnen te gebruiken kan de speler healen. 
Met nul health is het game over.

### Extra Features (indien tijd):
**Meer Rooms/Levels**
**Audio System**
**Save/Load Systeem**
**Text Boxes**

---


```
Welke techstack/libraries je zou willen gebruiken.
```

Ik heb gekeken naar welke libraries er gebruikt kunnen worden voor een spel maken met python, ik zag dat de library PyGame gebruikt kan worden voor 2d spellen, en na het kijken van voorbeelden van spellen die met pygame zijn gemaakt kan ik wel zien wat voor spel ik er mee kan maken.

**PyGame** - Hoofdlibrary voor graphics, geluid en input handling
https://www.pygame.org

**Pytest** - Voor unit en integration testing
https://docs.pytest.org/en/stable

**JSON** - Voor map data en save files
https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON

**Random** - Voor procedurele enemy behavior en spawning
https://docs.python.org/3/library/random.html

---

## Python Advanced: 

```
Leg uit welke onderdelen van de Python Advanced module je gaat toepassen. 
Dit kan bijvoorbeeld error handling zijn, OOP, of testing.
```

Ik ga dingen gebruiken als testing om heel veel unit en intergration tests te doen, ik weet nog niet hoe ik system tests ga doen, maar misschien kan ik dit nog later doen.

OOP word super belangrijk voor de game omdat je natuurlijk veel instanties gaat maken van alles, muren, enemies, de player, objecten, interactieve elementen.

---

## Planning: 

```
Geef in een tabel weer wat je per week gaat doen, en hoeveel uren/commits per week je hier ongeveer aan wilt besteden. Maak een reeele planning!
```

|Week   |Doel                                   |
|---    |---	                                |
|Week 1 |Concept maken                          |
|Week 2 |Concept Review + Implementatie         |
|Week 3 |Werkend prototype van kernmechanics    |
|Week 4 |Functionele iteratie                   |
|Week 5 |Content & Level Design	Speelbare room  |
|Week 6 |Tests Maken                            |
|Week 7 |Systemen afmaken en polishen	        |
|Week 8 |Presentatie maken / inleveren project  |


### Week 1

- Github Aanmaken
- Libraries opzoeken
- gameplay-loop 
- mechanics lichtcirkel, fog-of-war, vijanden 
- Functionele beschrijving opstellen. 
- Schets (handgetekend) voor structuur
- Concept Inleveren

### Week 2

- Review integreren in document.
- Folders maken
- Basis Pygame window + main loop opzetten.
- OOP-structuur bepalen (Player, Enemy, Map, LightSystem).
- GamePy Leren

### Week 3

- Player movement + collision detection met muren.
- Basis map loader (tile-based, zoals in Clock Tower / Fear and Hunger).
- Light circle.
- Fog-of-war eerste versie (surface overlay + alpha).
- Begin van enemy pathfinding (basic chase AI).

### Week 4

- health systeem.
- Inventory en interacties (bijv. sleutel oppakken, deur openen).
- Audio: ambient + jumpscare sounds.
- Verbeterde enemy AI idle / jagen / sleep mode
- Optimaliseren rendering (surface batching).

### Week 5
	
- Eerste room bouwen + triggers/ events.
- Extra assets maken/toevoegen (sprites, geluid).
- Ondersteuning voor meerdere maps.

- UI eerste versie (health bar, items, messages).
- Kijken of ik saving en loading in mijn game toe kan voegen
- Saving/loading prototype.

### Week 6

– Test voor collision-system.
- Error handling verbeteren (try/except/tests/loggen).
- Bugfixes.


### Week 7

- Systemen testen en afronden
- Polish 

### Week 8

- Presentatievideo opnemen (2–3 min: uitleg concept, gameplay demonstratie, code-structuur).
- Documentatie afronden: README, installatie, controls.
- Code indienen op Canvas.

### Per Week:
* 7 Commits
* 10 Uren

---

## Tests: 

```
Je moet ten minste 2 tests schrijven die ook wat toevoegen en bijvoegen bij je code. Wat voor tests ga je maken?
```

### Test 1: Player Collision Detection Test (Unit Test)
**Wat test ik:**
Deze test controleert of het collision-systeem correct werkt. Specifiek test ik of de speler niet door muren kan lopen en of de positie correct wordt teruggezet bij een collision.

**Voorbeeld testcases:**
- Test of speler stopt bij een muur (x-as)
- Test of speler stopt bij een muur (y-as)
- Test of speler wel kan bewegen in open ruimte
- Test of speler correct teruggeplaatst wordt na collision

### Test 3: Enemy Chase Behavior Test (Unit Test)
**Wat test ik:**
Deze test controleert of de enemy AI correct reageert op de speler. Specifiek test ik of een enemy van idle naar chase state gaat wanneer de speler binnen detection range komt.

**Voorbeeld testcases:**
- Test of enemy idle blijft wanneer speler ver weg is
- Test of enemy chase state ingaat wanneer speler dichtbij komt
- Test of enemy richting speler beweegt tijdens chase
- Test of enemy terugkeert naar patrol na speler kwijtraken
    

---

## Design: 

```
Maak een vluchtige schematische schets van je applicatie. Deze moet handgetekend zijn (mag niet digitaal). Neem hier een foto van en voeg deze toe in je word document.
```

---

## GitHub: 

```
Vermeld een link naar de GitHub of GitLab repository waar je je code gaat bewaren.
```

https://github.com/Tb27-27/Python_Game 