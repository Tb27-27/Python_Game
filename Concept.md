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

Het is een game die plaats vind in een cathedraal.

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
Welke techstack/libraries je zou willen gebruiken.
```

Ik heb gekeken naar welke libraries er gebruikt kunnen worden voor een spel maken met python, ik zag dat de library PyGame gebruikt kan worden voor 2d spellen.

https://www.pygame.org



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

|Week   |Doel                           |
|---    |---	                        |
|Week 1 |Concept maken                  |
|Week 2 |Concept Review + Implementatie |
|Week 3 |Werkend prototype van kernmechanics |
|Week 4 |Functionele iteratie           |
|Week 5 |Content & Level Design	Speelbare room                        |
|Week 6 |---	                        |
|Week 7 |---	                        |
|Week 8 |---	                        |


### Week 1

- Github Aanmaken
- Libraries opzoeken
- gameplay-loop 
- mechanics (lichtcirkel, fog-of-war, vijanden, inventaris). 
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

• Energie/health systeem.
• Inventory en interacties (bijv. sleutel oppakken, deur openen).
• Audio: ambient + jumpscare sounds.
• Verbeterde enemy AI (state machine: idle → chase → search).
• Optimaliseren rendering (surface batching).

### Week 5
	
- Eerste room bouwen + triggers/ events.
- Extra assets maken/toevoegen (sprites, geluid).
- Ondersteuning voor meerdere maps.

- UI eerste versie (health bar, items, messages).
- Kijken of ik saving en loading in mijn game toe kan voegen
- Saving/loading prototype.

### Week 6

### Week 7

### Week 8
	


Week 6 – Testing, Debugging, Python Advanced	Tests + codekwaliteitsronde	• Unit tests schrijven (minimaal 2 verplicht):
– Test voor collision-system.
– Test voor AI-state transitions.
• Error handling verbeteren (try/except + logging).
• Refactoring van modules en functies (SOLID).
• Pylint/Black formatter instellen.
• Bugfixes level & rendering.	6–8 uur	4–5
Week 7 – Afbouw + Quality Pass	Release candidate	• Finaliseren gameflow (startmenu → level → game over).
• Performance check (FPS stabiliteit).
• Polijsten visuals (licht, animaties, fog).
• Geluid mixen.
• Gameplaybalans (snelheid, zichtbaarheid, enemy ranges).	8 uur	4
Week 8 – Definitieve Inlevering & Presentatie	Definitieve code + presentatievideo (Stap 3)	• Kleine restwerkzaamheden oplossen.
• Presentatievideo opnemen (2–3 min: uitleg concept, gameplay demonstratie, code-structuur).
• Documentatie afronden: README, installatie, controls.
• Code indienen op Canvas.

Per Week:
* 7 Commits
* 10 Uren

---

## Tests: 

```
Je moet ten minste 2 tests schrijven die ook wat toevoegen en bijvoegen bij je code. Wat voor tests ga je maken?
```

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