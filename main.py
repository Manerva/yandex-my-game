import pygame
import sys

import json
import time
import datetime


pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игровое меню")

font = pygame.font.Font(None, 46)



def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

class Player:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.has_key = False
        self.start_time = 0
        self.end_time = 0
        self.levels = {
            1: [
                "####################",
                "##      F         @##",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",

            ],
            2: [
                "####################",
                "##                @##",
                "######   ###########",
                "###### F ###########",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",

            ],
            3: [
                "####################",
                "##        ##########",
                "####### ############",
                "#F####  ############",
                "#   ## #############",
                "###       ##########",
                "#########@##########",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",
                "####################",

            ],
            4: [
                "####################",
                "####   #   #   #    ",
                "#F   #   #   #   ###",
                "## #################",
                "##  ################",
                "### ################",
                "### #            ###",
                "### # ########## ###",
                "### # #@       # ###",
                "### # ######## # ###",
                "### #          # ###",
                "### ############ ###",
                "###              ###",
                "####################",

            ],
            5: [
                "###################@#",
                "#   ##    ##   #    #",
                "## ##  ## ## #   #####",
                "## ### ##    ###   ###",
                "##       #####   #####",
                "###### ####### #######",
                "#####==## #######  ##",
                "#     =#      ##  = ##",
                "# ######### ##### ###",
                "#   #######     #   #",
                "# ########## ## # ###",
                "#        #   ##F## ###",
                "# ######   # ##### ###",
                "######################",
                "######################",
                "######################"

            ],
        }

        self.current_level = level
        self.has_key = False
        self.spawn_positions = {
            1: (2, 1),
            2: (2, 1),
            3: (1, 1),
            4: (19, 1),
            5: (1, 1),
        }
        self.x, self.y = self.spawn_positions[self.current_level]

    def update_timer(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        return int(elapsed_time)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(self.levels[self.current_level][0]) and 0 <= new_y < len(self.levels[self.current_level]):
            if self.levels[self.current_level][new_y][new_x] != '#':
                self.x = new_x
                self.y = new_y

                if self.levels[self.current_level][new_y][new_x] == 'F':
                    self.has_key = True
                    self.levels[self.current_level][new_y] = self.levels[self.current_level][new_y][:new_x] + ' ' + self.levels[self.current_level][new_y][new_x+1:]

                if self.levels[self.current_level][new_y][new_x] == '@' and self.has_key:
                    self.show_win_screen()

    def show_win_screen(self):
        popup_width = 357
        popup_height = 219
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2

        json_file_path = f'level_{self.current_level}_best_time.json'
        best_time = None
        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

                if self.update_timer() < data['time']:
                    data['time'] = self.update_timer()
            
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file)

        except FileNotFoundError:
            with open(json_file_path, 'w') as json_file:
                data = {
                    "time": self.update_timer(),
                }
                json.dump(data, json_file)

        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        pygame.draw.rect(popup_surface, (255, 210, 210), (0, 0, popup_width, popup_height), border_radius=10)

        
        try:
            with open(json_file_path, 'r') as json_file:
                data_tm = json.load(json_file)
        except FileNotFoundError:
            pass

        draw_text("Вы успешно прошли уровень!", pygame.font.Font(None, 30), (0, 0, 0), popup_surface, popup_width // 2, 25)
        draw_text(f"Время прохождения: {self.update_timer()} сек.", pygame.font.Font(None, 20), (0, 0, 0), popup_surface, popup_width // 2, 50)
        draw_text(f"Лучшее время прохождения: {data_tm['time']}.", pygame.font.Font(None, 20), (0, 0, 0), popup_surface, popup_width // 2, 70)




        button_width = 80
        button_height = 30
        button_spacing = 20

        button2_rect = pygame.Rect((popup_width - button_width) // 2, 95, button_width, button_height)
        button1_rect = pygame.Rect((popup_width - button_width) // 2, 95 + button_height + button_spacing, button_width, button_height)

        button1_texture = pygame.image.load('data/next.png')
        button2_texture = pygame.image.load('data/menu.png')


        popup_surface.blit(button1_texture, button1_rect)
        popup_surface.blit(button2_texture, button2_rect)



        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        screen.blit(popup_surface, (popup_x, popup_y))
        pygame.display.flip()

        # Ожидание закрытия всплывающего окна
        waiting_for_close = True
        while waiting_for_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_x - popup_x, mouse_y - popup_y):
                        waiting_for_close = False
                        # Переход на следующий уровень
                        self.current_level += 1
                        # Проверка что уровни не закончились
                        if self.current_level > len(self.levels):
                            print("Поздравляем! Вы прошли все уровни!")
                            pygame.quit()
                            sys.exit()
                        else:
                            # Запуск следующего уровня
                            run_game(self.current_level)
                        waiting_for_close = False
                    elif button2_rect.collidepoint(mouse_x - popup_x, mouse_y - popup_y):
                        level_menu()
                        waiting_for_close = False


def main_menu():
    while True:
        background_main = pygame.image.load('data/background_main.png')
        screen.blit(background_main, (0, 0))

        draw_text("Главное меню", font, (0, 0, 0), screen, 400, 100)

        play_button_image = pygame.image.load('data/start_button.png')
        play_button_rect = play_button_image.get_rect(topleft=(300, 225))
        screen.blit(play_button_image, play_button_rect.topleft)

        exit_button_image = pygame.image.load('data/exit_button.png')
        exit_button_rect = exit_button_image.get_rect(topleft=(300, 325))
        screen.blit(exit_button_image, exit_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    level_menu()
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def level_menu():
    rows = 3  # К строк
    cols = 3  # К столбцов
    button_size = 80  # рзкнопки

    background_levels = pygame.image.load('data/background_levels.png')
    screen.blit(background_levels, (0, 0))

    draw_text("Выбор уровня", font, black, screen, 400, 100)

    table_width = cols * button_size + (cols - 1) * 20
    table_height = rows * button_size + (rows - 1) * 20
    table_x = (screen_width - table_width) // 2
    table_y = (screen_height - table_height) // 2

    level_buttons = []
    for i in range(rows):
        for j in range(cols):
            button = pygame.Rect(table_x + j * (button_size + 20), table_y + i * (button_size + 20), button_size, button_size)
            play_button_image = pygame.image.load(f'data/level_{i * cols + j + 1}.png')
            level_buttons.append(button)
            screen.blit(play_button_image, button.topleft)

    back_button_image = pygame.image.load('data/back_button.png')
    back_button_rect = back_button_image.get_rect(topleft=(10, 10))
    screen.blit(back_button_image, back_button_rect.topleft)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(level_buttons):
                    if button.collidepoint(event.pos):
                        print(f"Запущен уровень {i + 1}")
                        run_game(i + 1)
                if back_button_rect.collidepoint(event.pos):
                    main_menu()

        pygame.display.update()

def run_game(level):
    CELL_SIZE = 40

    player_texture = pygame.image.load('data/player.png')
    key_texture = pygame.image.load('data/key.png')
    door_texture =  pygame.image.load('data/door.png')
    block_wall_texture =  pygame.image.load('data/block_wall.png') 
    empty_inventory_texture = pygame.image.load('data/empty_inventory.png')
    inventory_key_texture = pygame.image.load('data/inventory_key.png')



    player = Player(1, 1, level)
    player.start_time = time.time()

 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
        elapsed_time = player.update_timer()
        screen.fill((90, 120, 147))
        pygame.draw.rect(screen, (90, 120, 147), (0, 0, screen_width, 50))
        
        # inventory
        if player.has_key:
            screen.blit(inventory_key_texture, (10, 10))
        else:
            screen.blit(empty_inventory_texture, (10, 10))

        elapsed_time = player.update_timer()
        inventory_text = font.render(f"Время: {elapsed_time} сек", True, (46, 54, 63))
        screen.blit(inventory_text, (50, 10))

        for y, row in enumerate(player.levels[player.current_level]):
            for x, cell in enumerate(row):
                if cell == '#':
                    screen.blit(block_wall_texture, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
                elif cell == 'F':
                    screen.blit(key_texture, (x * CELL_SIZE, y * CELL_SIZE + 50))
                elif cell == '@':
                    screen.blit(door_texture, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
                elif cell == '=':
                    screen.blit(block_wall_texture, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))

        screen.blit(player_texture, (player.x * CELL_SIZE, player.y * CELL_SIZE + 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()