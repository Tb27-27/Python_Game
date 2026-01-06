import pygame
import random
from src.colors import *

class CellphoneInterface:
    def __init__(self, screen_width_pixels, screen_height_pixels, active_logic_module):
        # dit is de basis van de telefoon die de minigames laat zien
        self.is_active = True
        self.current_application = active_logic_module
        self.display_width_pixels = active_logic_module.display_width_pixels
        self.display_height_pixels = active_logic_module.display_height_pixels
        
        # bereken de ruimte voor de randen van de telefoon
        self.phone_padding_pixels = 20
        self.phone_width_pixels = self.display_width_pixels + (self.phone_padding_pixels * 2)
        self.phone_height_pixels = self.display_height_pixels + 80
        
        # zorg dat de telefoon precies in het midden van het scherm staat
        self.base_position_coordinate_x = (screen_width_pixels - self.phone_width_pixels) // 2
        self.base_position_coordinate_y = (screen_height_pixels - self.phone_height_pixels) // 2
        
        # variabelen voor het schudden van de telefoon bij fouten
        self.shake_timer_frames = 0
        self.display_surface = pygame.Surface((self.display_width_pixels, self.display_height_pixels))

    def handle_input(self, event):
        # geef de toetsenbordinvoer door aan de actieve minigame
        if self.current_application:
            self.current_application.handle_input(event)

    def update(self):
        # werk de logica van de minigame bij
        if self.current_application:
            self.current_application.update()
            
            # als de minigame vraagt om te schudden zetten we de timer aan
            if getattr(self.current_application, "shake_requested", False):
                self.shake_timer_frames = 15
                self.current_application.shake_requested = False
                
            # sluit de interface als de minigame klaar is
            if not self.current_application.is_active:
                self.is_active = False
        
        # tel de schudtimer af naar nul
        if self.shake_timer_frames > 0:
            self.shake_timer_frames -= 1

    def draw(self, main_surface):
        # bereken de positie en voeg willekeurige beweging toe als de telefoon schudt
        render_x = self.base_position_coordinate_x
        render_y = self.base_position_coordinate_y
        
        if self.shake_timer_frames > 0:
            render_x += random.randint(-7, 7)
            render_y += random.randint(-7, 7)
            
        # teken de buitenkant van de telefoon met afgeronde hoeken
        phone_rect = pygame.Rect(render_x, render_y, self.phone_width_pixels, self.phone_height_pixels)
        pygame.draw.rect(main_surface, (25, 25, 25), phone_rect, border_radius=30)
        pygame.draw.rect(main_surface, GRAY, phone_rect, 3, border_radius=30)
        
        # teken de inhoud van de minigame op het zwarte schermpje
        self.display_surface.fill(BLACK)
        if self.current_application:
            self.current_application.draw(self.display_surface)
            
        # blit het schermpje op de juiste plek binnen de behuizing
        main_surface.blit(self.display_surface, (render_x + self.phone_padding_pixels, render_y + 50))

class FallingOperator:
    def __init__(self, width_pixels, python_operators_list, fake_operators_list):
        # deze klasse maakt een vallend tekstobject aan
        self.is_python_operator = random.choice([True, False])
        if self.is_python_operator:
            self.text_content = random.choice(python_operators_list)
        else:
            self.text_content = random.choice(fake_operators_list)
            
        self.position_coordinate_x = random.randint(30, width_pixels - 60)
        self.position_coordinate_y = -50
        self.movement_speed = random.uniform(2.0, 4.0)
        self.font_style = pygame.font.Font(None, 28)

    def update(self):
        # laat het object zakken
        self.position_coordinate_y += self.movement_speed

    def draw(self, surface):
        # kies de kleur op basis van of het een echte python operator is
        text_color = LIGHT_BLUE if self.is_python_operator else WHITE
        rendered_text = self.font_style.render(self.text_content, True, text_color)
        surface.blit(rendered_text, (self.position_coordinate_x, self.position_coordinate_y))

class OperatorMinigame:
    def __init__(self, width_pixels, height_pixels):
        # instellingen voor het schietspelletje
        self.display_width_pixels = width_pixels
        self.display_height_pixels = height_pixels
        self.is_active = True
        self.total_score_points = 0
        self.shake_requested = False
        self.player_position_x = width_pixels // 2
        self.projectiles_list = []
        self.enemies_list = []
        self.spawn_timer_frames = 0
        
        # lijsten met goede en foute antwoorden
        self.python_operators = [
            "+", "-", "*", "/", "**", "//", "%", 
            "==", "!=", ">", "<", ">=", "<=", 
            "and", "or", "not", "is", "in", 
            "+=", "-="
        ]
        
        self.fake_operators = [
            "&&", "||", "!", "===", "!==", "++", "--", 
            "->", "=>", "::", "?.", "??", "<<<", 
            "instanceof", "typeof", "var", "let", 
            "begin", "end", "nil"
        ]

    def handle_input(self, event):
        # schiet met de spatiebalk
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.projectiles_list.append({"x": self.player_position_x, "y": self.display_height_pixels - 60, "speed": 12})

    def update(self):
        # beweging van de speler met de pijltjestoetsen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.player_position_x = max(20, self.player_position_x - 6)
        if keys[pygame.K_RIGHT]: self.player_position_x = min(self.display_width_pixels - 20, self.player_position_x + 6)
        
        # beheer het spawnen van nieuwe vijanden
        self.spawn_timer_frames += 1
        if self.spawn_timer_frames >= 45:
            self.enemies_list.append(FallingOperator(self.display_width_pixels, self.python_operators, self.fake_operators))
            self.spawn_timer_frames = 0
            
        # werk projectielen bij en verwijder ze als ze buiten beeld zijn
        for projectile in self.projectiles_list[:]:
            projectile["y"] -= projectile["speed"]
            if projectile["y"] < 0: self.projectiles_list.remove(projectile)
            
        # controleer op botsingen tussen kogels en tekst
        for enemy in self.enemies_list[:]:
            enemy.update()
            enemy_rect = pygame.Rect(enemy.position_coordinate_x, enemy.position_coordinate_y, 40, 30)
            for projectile in self.projectiles_list[:]:
                if enemy_rect.collidepoint(projectile["x"], projectile["y"]):
                    if not enemy.is_python_operator:
                        self.total_score_points += 20
                    else:
                        self.total_score_points = max(0, self.total_score_points - 15)
                        self.shake_requested = True
                    if enemy in self.enemies_list: self.enemies_list.remove(enemy)
                    if projectile in self.projectiles_list: self.projectiles_list.remove(projectile)
            if enemy.position_coordinate_y > self.display_height_pixels: self.enemies_list.remove(enemy)
        
        # eindig het spel bij honderd punten
        if self.total_score_points >= 100: self.is_active = False

    def draw(self, surface):
        # teken de speler en de kogels
        pygame.draw.rect(surface, GREEN, (self.player_position_x - 15, self.display_height_pixels - 60, 30, 20))
        for projectile in self.projectiles_list:
            pygame.draw.circle(surface, WHITE, (int(projectile["x"]), int(projectile["y"])), 4)
        for enemy in self.enemies_list: enemy.draw(surface)
        
        # toon de huidige score onderaan
        score_font = pygame.font.Font(None, 24)
        score_text = score_font.render(f"score {self.total_score_points} van 100", True, GREEN)
        surface.blit(score_text, (10, self.display_height_pixels - 30))

class PythonTrackMinigame:
    def __init__(self, width_pixels, height_pixels):
        # instellingen voor het racespel
        self.display_width_pixels = width_pixels
        self.display_height_pixels = height_pixels
        self.is_active = True
        self.total_score_points = 0
        self.shake_requested = False
        self.current_lane_index = 0
        self.spawn_timer_frames = 0
        self.falling_objects_list = []
        self.commands_list = [
            ("print('ok')", "echo 'no'"),
            ("len(a)", "a.size()"),
            ("if a == 1:", "if a = 1:"),
            ("def func():", "function func()"),
            ("import math", "include math"),
            ("elif x == 2:", "else if x == 2:"),
            ("True", "true"),
            ("None", "null"),
            ("list.append(1)", "list.push(1)"),
            ("for i in range(5):", "for(i=0;i<5;i++)"),
            ("while x < 5:", "while(x < 5) {"),
            ("int('5')", "(int)'5'"),
            ("x in list", "list.contains(x)"),
            ("type(x)", "typeof(x)"),
            ("bool(1)", "boolean(1)"),
            ("[1, 2, 3]", "{1, 2, 3}"),
            ("math.pi", "math->pi"),
            ("input('name')", "get('name')"),
            ("isinstance(x, int)", "x instanceof int")
        ]

    def handle_input(self, event):
        # wissel van baan met de pijltjes of a en d
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a): self.current_lane_index = 0
            if event.key in (pygame.K_RIGHT, pygame.K_d): self.current_lane_index = 1

    def update(self):
        # maak elke 120 frames / 2 seconden een nieuw paar commando s aan
        self.spawn_timer_frames += 1
        if self.spawn_timer_frames >= 120:
            correct_text, wrong_text = random.choice(self.commands_list)
            lane_position = random.randint(0, 1)
            self.falling_objects_list.append({'text': correct_text, 'is_correct': True, 'lane': lane_position, 'y': -30})
            self.falling_objects_list.append({'text': wrong_text, 'is_correct': False, 'lane': 1 - lane_position, 'y': -30})
            self.spawn_timer_frames = 0
            
        # beweeg de objecten en controleer of de speler ze raakt
        for obj in self.falling_objects_list[:]:
            obj['y'] += 1
            if self.display_height_pixels - 100 < obj['y'] < self.display_height_pixels - 40 and obj['lane'] == self.current_lane_index:
                if obj['is_correct']:
                    self.total_score_points += 25
                else:
                    self.total_score_points = max(0, self.total_score_points - 20)
                    self.shake_requested = True
                self.falling_objects_list.remove(obj)
            elif obj['y'] > self.display_height_pixels:
                self.falling_objects_list.remove(obj)
                
        # stop het spel bij voldoende punten
        if self.total_score_points >= 100: self.is_active = False

    def draw(self, surface):
        # teken de scheidingslijn tussen de banen
        pygame.draw.line(surface, GRAY, (self.display_width_pixels // 2, 0), (self.display_width_pixels // 2, self.display_height_pixels), 2)
        
        # teken de speler in de huidige baan
        lane_center_x = (self.current_lane_index * (self.display_width_pixels // 2)) + (self.display_width_pixels // 4)
        pygame.draw.rect(surface, LIGHT_BLUE, (lane_center_x - 20, self.display_height_pixels - 80, 40, 20))
        
        # teken alle vallende commando s
        font_style = pygame.font.Font(None, 22)
        for obj in self.falling_objects_list:
            text_surface = font_style.render(obj['text'], True, WHITE)
            text_x = (obj['lane'] * (self.display_width_pixels // 2)) + (self.display_width_pixels // 4)
            surface.blit(text_surface, text_surface.get_rect(center=(text_x, obj['y'])))
            
        # toon de score onderaan
        score_text = font_style.render(f"score {self.total_score_points} of 100", True, GREEN)
        surface.blit(score_text, (10, self.display_height_pixels - 30))

class PythonQuizMinigame:
    def __init__(self, width_pixels, height_pixels):
        # instellingen voor de quiz
        self.display_width_pixels = width_pixels
        self.display_height_pixels = height_pixels
        self.is_active = True
        self.total_score_points = 0
        self.shake_requested = False
        self.current_question_index = 0
        self.feedback_timer_frames = 0
        self.feedback_message = ""
        
        # lijst met vragen en antwoord opties
        self.questions_data = [
            {"q": "what is 10 // 3 in python", "o": ["1. 3.33", "2. 3", "3. 1"], "c": 1},
            {"q": "how do you add an item to a list", "o": ["1. .append()", "2. .add()", "3. .push()"], "c": 0},
            {"q": "what is the symbol for a dictionary", "o": ["1. []", "2. ()", "3. {}"], "c": 2},
            {"q": "what is the output of 2 ** 3", "o": ["1. 6", "2. 8", "3. 9"], "c": 1},
            {"q": "which keyword starts a function", "o": ["1. function", "2. def", "3. define"], "c": 1},
            {"q": "how to check the length of a string", "o": ["1. len()", "2. count()", "3. size()"], "c": 0},
            {"q": "what does bool(0) return", "o": ["1. True", "2. False", "3. None"], "c": 1},
            {"q": "which one is a tuple", "o": ["1. (1, 2)", "2. [1, 2]", "3. {1, 2}"], "c": 0},
            {"q": "how to run a loop five times", "o": ["1. range(4)", "2. range(5)", "3. range(6)"], "c": 1},
            {"q": "how to import a library", "o": ["1. use math", "2. include math", "3. import math"], "c": 2},
            {"q": "what symbol is used for comments", "o": ["1. //", "2. #", "3. --"], "c": 1},
            {"q": "how to change a string to an integer", "o": ["1. int()", "2. str()", "3. float()"], "c": 0},
            {"q": "what is the type of 5.5", "o": ["1. int", "2. string", "3. float"], "c": 2},
            {"q": "how to remove the last item of a list", "o": ["1. .delete()", "2. .pop()", "3. .remove()"], "c": 1},
            {"q": "how to write a multiline string", "o": ["1. '''text'''", "2. //text//", "3. --text--"], "c": 0},
            {"q": "which operator checks for equality", "o": ["1. =", "2. is", "3. =="], "c": 2},
            {"q": "which is a valid variable name", "o": ["1. 1_var", "2. my_var", "3. my-var"], "c": 1},
            {"q": "what does strip() do", "o": ["1. remove spaces", "2. cut text", "3. delete text"], "c": 0},
            {"q": "how to make an empty set", "o": ["1. set()", "2. {}", "3. []"], "c": 0},
            {"q": "what is the result of 10 % 3", "o": ["1. 3", "2. 1", "3. 0"], "c": 1}
        ]

        random.shuffle(self.questions_data)

    def handle_input(self, event):
        # verwerk de antwoord keuze van de speler
        if self.feedback_timer_frames > 0 or event.type != pygame.KEYDOWN:
            return
            
        choice_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2}
        player_choice = choice_map.get(event.key, -1)
        
        if player_choice != -1:
            correct_answer = self.questions_data[self.current_question_index]["c"]
            if player_choice == correct_answer:
                self.total_score_points += 25
                self.feedback_message = "Well done"
            else:
                self.total_score_points = max(0, self.total_score_points - 15)
                self.shake_requested = True
                self.feedback_message = "WRONG"
            self.feedback_timer_frames = 45

    def update(self):
        # toon feedback en ga daarna naar de volgende vraag
        if self.feedback_timer_frames > 0:
            self.feedback_timer_frames -= 1
            if self.feedback_timer_frames == 0:
                self.current_question_index += 1
                self.feedback_message = ""
                if self.current_question_index >= len(self.questions_data) or self.total_score_points >= 100:
                    self.is_active = False

    def draw(self, surface):
        # fonts voor de tekst
        question_font = pygame.font.Font(None, 28)
        option_font = pygame.font.Font(None, 24)
        
        # teken de huidige vraag en opties
        if self.current_question_index < len(self.questions_data):
            current_question_data = self.questions_data[self.current_question_index]
            surface.blit(question_font.render(current_question_data["q"], True, WHITE), (20, 50))
            for index, option in enumerate(current_question_data["o"]):
                surface.blit(option_font.render(option, True, LIGHT_BLUE), (30, 120 + index * 70))
                
        if self.feedback_message:
            if "well done" in self.feedback_message.lower(): 
                feedback_color = GREEN 
            else: 
                feedback_color = RED
                
            feedback_surface = question_font.render(self.feedback_message, True, feedback_color)
            
            # bereken de positie voor het midden van het scherm
            render_coordinate_x = self.display_width_pixels // 2 - 40
            render_coordinate_y = self.display_height_pixels - 100
            surface.blit(feedback_surface, (render_coordinate_x, render_coordinate_y))
            
        # toon de voortgang van de score onderaan het scherm
        score_status_text = f"score {self.total_score_points} van 100"
        progress_text = option_font.render(score_status_text, True, WHITE)
        surface.blit(progress_text, (10, self.display_height_pixels - 30))