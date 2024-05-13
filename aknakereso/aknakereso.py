
import pygame
import sys
import random
import time
import numpy
from pygame.math import Vector2

cell_size = 60
cell_number = 10
cell_left = 100
bomb_number = 10
left_bomb_number = 10
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * (cell_number + 1)))

class MAIN_GAME:
    def __init__(self):
        self.cells = CELLS()
        self.time = TIME()
        self.leftbombs = LEFTBOMBS()
        self.exit = EXIT()
        self.table = TABLE()
        self.bombs = []
        self.pins = []
        self.numbercells = NUMBERCELLS(self)
        self.game_over = False
        self.won_game = False
        self.first_click = True
        self.lose = False
        self.cells_not_revealed = 0
        self.adj_cell_number = 0 
        self.start_time = time.time() 
        self.minutes = 0
        self.seconds = 0
        self.end_printed = False

    def draw_elements(self):
        if not self.game_over and not self.won_game:
            self.time.print_time()
            self.leftbombs.print_leftbombs()
            self.leftbombs.draw_leftbombs()
        self.exit.draw_exit()
        if self.first_click:
            self.cells.draw_cells()
            self.table.draw_table()
        else:
            for bomb in self.bombs:
                bomb.draw_bomb()
            self.numbercells.draw_numbercells()
            self.cells.draw_cells()
            self.table.draw_table()
            for pin in self.pins:
                center_x = int(pin[0] * cell_size + cell_size / 2)
                center_y = int(pin[1] * cell_size + cell_size / 2)
                pygame.draw.circle(screen, (165, 42, 42), (center_x, center_y), (cell_size // 2) - 2)

    def click_cell(self):  
        global bomb_number
        global left_bomb_number
    
        mouse_pos = pygame.mouse.get_pos()
        clicked_cell = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)

        if not self.end_printed:
            if self.first_click:
                try:
                    self.exit.check_click(mouse_pos)
                    self.cells.positions.remove(clicked_cell)
                    clicked_adjacent_cells = [
                        (clicked_cell[0] + dx, clicked_cell[1] + dy)
                        for dx in (-1, 0, 1)
                        for dy in (-1, 0, 1)
                        if (dx != 0 or dy != 0) and (clicked_cell[0] + dx, clicked_cell[1] + dy) in self.cells.positions
                    ]   
                    for pos in clicked_adjacent_cells:
                        self.cells.positions.remove(pos)
                    global cell_left
                    cell_left -= 1
                    self.occupied_positions = set(self.cells.positions)
                    self.bombs = [BOMBS(self.occupied_positions) for _ in range(bomb_number)]
                    for cell in clicked_adjacent_cells:
                        cell_left -= 1
                        if self.numbercells.bombs_adjacent(cell) == 0:
                            self.reveal_adjacent_cells(cell)
                    self.first_click = False
                except ValueError:
                    pass
            else:
                if clicked_cell in self.pins:
                    return
                elif clicked_cell in self.cells.positions:
                    self.adjacent_cells(clicked_cell)
                    try:
                        self.cells.positions.remove(clicked_cell)
                        cell_left -= 1
                    except ValueError:
                        pass

                    if self.numbercells.bombs_adjacent(clicked_cell) == 0:
                        self.reveal_adjacent_cells(clicked_cell)
                else:
                    self.exit.check_click(mouse_pos)
            if not self.first_click:
                if cell_left == bomb_number:
                    self.won_game = True
        else:
            self.exit.check_click(mouse_pos)


    def adjacent_cells(self,cell):
        cells_adjancent = [
            (cell[0] + dx, cell[1] + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx != 0 or dy != 0)
        ]
        self.cells_not_revealed = 0
        self.adj_cell_number = 0
        for pos in cells_adjancent:
            if (pos[0] >= 0 and pos[0] < cell_number) and (pos[1] >= 1 and pos[1] < cell_number+1):
                if pos in self.cells.positions:
                    self.cells_not_revealed += 1
                self.adj_cell_number += 1

    def reveal_adjacent_cells(self, cell):
        global left_bomb_number
        adjacent_cells = [
            (cell[0] + dx, cell[1] + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx != 0 or dy != 0) and (cell[0] + dx, cell[1] + dy) in self.cells.positions
        ]
        for adjacent_cell in adjacent_cells:
            if adjacent_cell in self.cells.positions:
                self.cells.positions.remove(adjacent_cell)
                global cell_left
                cell_left -= 1
                if adjacent_cell in self.pins:
                    self.pins.remove(adjacent_cell)
                    left_bomb_number += 1
                if self.numbercells.bombs_adjacent(adjacent_cell) == 0:
                    self.reveal_adjacent_cells(adjacent_cell)

    def check_bomb(self):
        if self.game_over:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        clicked_cell = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
        for bomb in self.bombs:
            if clicked_cell == bomb.pos:
                for bomb in self.bombs:
                    if clicked_cell == bomb.pos:
                        if clicked_cell not in self.pins:
                            self.game_over = True
                        return

    def draw_pin(self):
        global left_bomb_number
        global bomb_number
        mouse_pos = pygame.mouse.get_pos()
        clicked_cell = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
        if clicked_cell in self.cells.positions:
            if clicked_cell in self.pins:
                self.pins.remove(clicked_cell)
                left_bomb_number += 1
            else:
                self.pins.append(clicked_cell)
                left_bomb_number -= 1
    
    def end_time(self):
        elapsed_time = time.time() - self.start_time
        self.minutes = int(elapsed_time // 60)
        self.seconds = int(elapsed_time % 60)
    
    def check_win(self):
        global cell_left
        global left_bomb_number
        if self.won_game:
            if not self.end_printed:
                self.end_time()
                win_str = "Nyertél :)"
                time_str = f"Idő: {self.minutes:02}:{self.seconds:02}"
                font = pygame.font.SysFont('comicsansms', 45)
                text_win = font.render(win_str, True, (0, 200, 0))
                text_time = font.render(time_str, True, (0, 200, 0))
                win_rect = text_win.get_rect()
                time_rect = text_time.get_rect()
                win_rect.midleft = (40,25)
                time_rect.midright = (500,25)
                screen.blit(text_win, win_rect)
                screen.blit(text_time, time_rect)
                pygame.display.update()
                self.end_printed = True

    def check_lose(self):
        global cell_left
        global left_bomb_number
        if self.game_over:
            if not self.end_printed: 
                lose_str = "Vesztettél :("
                font = pygame.font.SysFont('comicsansms', 45)
                text_lose = font.render(lose_str, True, (255, 0, 0))
                lose_rect = text_lose.get_rect()
                lose_rect.center = (270,25)
                screen.blit(text_lose, lose_rect)
                for bomb in self.bombs:
                    bomb.draw_bomb()
                pygame.display.update()
                self.end_printed = True

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_cell()
            self.check_bomb()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.draw_pin() 


class TIME:
    def __init__(self):
        self.font = pygame.font.SysFont('britannic', cell_size-2)  
        self.start_ticks = pygame.time.get_ticks()  

    def print_time(self):
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_str = f'{minutes:02d}:{seconds:02d}'
        text = self.font.render(time_str, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.midleft = (0*cell_size+2,(1/2)*cell_size)
        screen.blit(text, text_rect)

class LEFTBOMBS:
    def __init__(self):
        self.font = pygame.font.SysFont('britannic', cell_size-2)
        self.x = (cell_number*cell_size)*(1/2)-(1/2)*cell_size
        self.y = 1/2*cell_size
        self.pos = Vector2(self.x,self.y)

    def draw_leftbombs(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), (cell_size // 2)-2)
    
    def print_leftbombs(self):
        bomb_str = f':{left_bomb_number}'
        text = self.font.render(bomb_str, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.midleft = (cell_number*cell_size*(1/2),(1/2)*cell_size)
        screen.blit(text,text_rect)
        
class EXIT:
    def __init__(self):
        self.font = pygame.font.SysFont('britannic', cell_size-2)
        self.x = (cell_number*cell_size)-(1/2)*cell_size
        self.y = 1/2*cell_size
        self.pos = Vector2(self.x, self.y)

    def draw_exit(self):
        pygame.draw.circle(screen, (0, 123, 0), (int(self.pos.x), int(self.pos.y)), (cell_size // 2) - 2)
        pygame.draw.line(screen, (255, 255, 255), (int(self.pos.x) - (cell_size // 4), int(self.pos.y) - (cell_size // 4)), (int(self.pos.x) + (cell_size // 4), int(self.pos.y) + (cell_size // 4)), 5)
        pygame.draw.line(screen, (255, 255, 255), (int(self.pos.x) + (cell_size // 4), int(self.pos.y) - (cell_size // 4)), (int(self.pos.x) - (cell_size // 4), int(self.pos.y) + (cell_size // 4)), 5)

    def check_click(self, mouse_pos):
        exit_rect = pygame.Rect(self.pos.x - (cell_size // 2), self.pos.y - (cell_size // 2), cell_size, cell_size)
        if exit_rect.collidepoint(mouse_pos):
            import runner.py

class BOMBS:
    def __init__(self, occupied_positions):
        self.occupied_positions = occupied_positions
        self.generate_position()

    def generate_position(self):
        while True:
            pos = random.choice(list(self.occupied_positions))
            self.occupied_positions.remove(pos)
            self.pos = Vector2(*pos)
            break

    def draw_bomb(self):
        center_x = int(self.pos[0] * cell_size + cell_size / 2)
        center_y = int(self.pos[1] * cell_size + cell_size / 2)
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), (cell_size // 2)-2)

class CELLS:
    def __init__(self):
        self.x = range(0, cell_number)
        self.y = range(1, cell_number+1) 
        self.positions = [(x, y) for x in self.x for y in self.y]

    def draw_cells(self):
        for pos in self.positions:
            cell_rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 196, 203), cell_rect)

class NUMBERCELLS:
    def __init__(self, main_game):
        self.font = pygame.font.SysFont('britannic', cell_size-2)
        self.main_game = main_game
        self.x = range(0, cell_number)
        self.y = range(1, cell_number+1) 
        self.positions = [(x, y) for x in self.x for y in self.y]

    def bombs_adjacent(self, pos):
        bomb_adj = 0
        adj_bomb_pos = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
            (pos[0] + 1, pos[1] + 1),
            (pos[0] - 1, pos[1] - 1),
            (pos[0] + 1, pos[1] - 1),
            (pos[0] - 1, pos[1] + 1)
        ]
        for adj_pos in adj_bomb_pos:
            if adj_pos in [bomb.pos for bomb in self.main_game.bombs]:
                bomb_adj += 1
        return bomb_adj

    def draw_numbercells(self):
        for pos in self.positions:
            if pos not in [bomb.pos for bomb in self.main_game.bombs]:
                bomb_adj = self.bombs_adjacent(pos)
                if bomb_adj != 0:
                    numbercell_rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
                    text = self.font.render(f'{bomb_adj}', True, (0, 0, 255))
                    text_rect = text.get_rect(center=(numbercell_rect.centerx, numbercell_rect.centery))
                    screen.blit(text, text_rect)

class TABLE:
    def __init__(self):
        self.x = range(0, cell_number)
        self.y = range(1, cell_number+1) 
        self.positions = [(x, y) for x in self.x for y in self.y]

    def draw_table(self):
        for pos in self.positions:
            table_rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), table_rect, width = 1)

pygame.init()
pygame.display.set_caption("Aknakereső")
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * (cell_number + 1)))
clock = pygame.time.Clock()

main_game = MAIN_GAME()

try:
    while True:
        if not main_game.end_printed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    main_game.handle_click(event)

            screen.fill((255, 255, 204))
            main_game.draw_elements()
            main_game.check_lose()
            main_game.check_win()
            pygame.display.update()
            clock.tick(60)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    main_game.handle_click(event)
except Exception as e:
    print(e)
    pygame.quit()
    sys.exit()