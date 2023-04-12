import pygame
from random import choice, randint, shuffle
from settings import *
from copy import deepcopy
import datetime
import time

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Sudoku')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/SourceSansPro-Regular.ttf', 50)
        self.win_font = pygame.font.Font('fonts/SourceSansPro-Regular.ttf', 100)
        self.time_font = pygame.font.Font('fonts/SourceSansPro-Regular.ttf', 30)

        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.init_grid()
        self.selected_col = 0
        self.selected_row = 0

        self.win = False
        self.win_time = time.time()
    
    def fill_box(self, box_number):
        i = int(box_number / 3) * 3
        j = box_number % 3 * 3
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(i, i + 3):
            for col in range(j, j + 3):
                self.grid[row][col] = choice(numbers)
                numbers.remove(self.grid[row][col])
    
    def find_empty(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.grid[i][j] == 0:
                    return (i, j)
        return (None, None)

    def remove_elemnts(self, num_of_elemnts_to_remove):
        cell_coords = []
        for _ in range(num_of_elemnts_to_remove):
            row, col = randint(0, 8), randint(0, 8)
            while (row, col) in cell_coords:
                row, col = randint(0, 8), randint(0, 8)
            self.grid[row][col] = 0
            cell_coords.append((row, col))

    # Check number validity
    def check_row_safety(self, num, i, j):
        for col, cell in enumerate(self.grid[i]):
            if num == cell and col != j:
                return False
        return True

    def check_col_safety(self, num, i, j):
        for row in range(ROWS):
            if num == self.grid[row][j] and row != i:
                return False
        return True
    
    def check_box_safety(self, num, i, j):
        num_i = i
        num_j = j
        i = int(i / 3) * 3
        j = int(j / 3) * 3
        for row in range(i, i + 3):
            for col in range(j, j + 3):
                if self.grid[row][col] == num and not(i == num_i and j == num_j):
                    return False
        return True
    
    def check_safety(self, num, i, j):
        return self.check_row_safety(num, i, j) and self.check_col_safety(num, i, j) and self.check_box_safety(num, i, j)
    
    def solve(self, i, j):
        if self.check_win():
            self.solved_grid = deepcopy(self.grid)
            return True

        if i != None and j != None:
            shuffle(self.numbers)
            for num in self.numbers:
                if self.check_safety(num, i, j):
                    self.grid[i][j] = num
                    row, col = self.find_empty()
                    if self.solve(row, col):
                        return True
                self.grid[i][j] = 0
            return False
    
    def init_grid(self):
        for i in range(0, 9, 4):
            self.fill_box(i)
        
        i, j = self.find_empty()
        self.solve(i, j)
        
        self.remove_elemnts(30)
        self.fixed_grid = deepcopy(self.grid)

    def highlight_current(self):
        horizontal_rect = pygame.Rect(0, self.selected_row * (TILE_SIZE + 1) + 1, WIDTH, TILE_SIZE)
        pygame.draw.rect(self.surface, SELECTED_ROW_COL, horizontal_rect)

        vertical_rect = pygame.Rect(self.selected_col * (TILE_SIZE + 1) + 1, 0, TILE_SIZE, HEIGHT)
        pygame.draw.rect(self.surface, SELECTED_ROW_COL, vertical_rect)

        cell_rect = pygame.Rect(self.selected_col * (TILE_SIZE + 1) + 1, self.selected_row * (TILE_SIZE + 1) + 1, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.surface, SELECTED_CELL, cell_rect)

    def render_text(self, number, col, row):
        number = self.font.render(str(number), True, BLUE)
        number_rect = number.get_rect()
        x, y = col * (TILE_SIZE + 1) + TILE_SIZE / 2 + 1, row * (TILE_SIZE + 1) + TILE_SIZE / 2 + 1
        number_rect.center = (x, y)
        self.surface.blit(number, number_rect.topleft)
    
    def draw_grid(self):
        self.surface.fill(WHITE)

        self.highlight_current()

        # Draw veritcal lines
        for i in range(1, 4):
            x = (i - 1) * 3 * (TILE_SIZE + 1) + 61
            pygame.draw.line(self.surface, LINES, (x, 0), (x, HEIGHT))
            pygame.draw.line(self.surface, LINES, (x + 61, 0), (x + 61, HEIGHT))

        # Draw horizontal lines
        for i in range(4):
            y = (i - 1) * 3 * (TILE_SIZE + 1) + 61
            pygame.draw.line(self.surface, LINES, (0, y), (WIDTH, y))
            pygame.draw.line(self.surface, LINES, (0, y + 61), (WIDTH, y + 61))

        # Draw vertical borders
        for i in range(1, 5):
            x = (i - 1) * 3 * (TILE_SIZE + 1)
            pygame.draw.line(self.surface, BLUE, (x, 0), (x, HEIGHT))
        
        # Draw horizontal borders
        for i in range(1, 5):
            y = (i - 1) * 3 * (TILE_SIZE + 1)
            pygame.draw.line(self.surface, BLUE, (0, y), (WIDTH, y))

        # Draw numbers
        for i in range(ROWS):
            for j in range(COLS):
                if self.grid[i][j]:
                    self.render_text(self.grid[i][j], j, i)

    def draw_win_screen(self):
        self.surface.fill(BACKGROUND)
        
        win_text = self.win_font.render('You Win!', True, WHITE)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)

        time_text = self.time_font.render(f'Time            {datetime.timedelta(seconds=self.win_time)}', True, WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 20)
        
        self.surface.blit(win_text, win_text_rect.topleft)
        self.surface.blit(time_text, time_text_rect.topleft)

    # Check for win
    def check_horizontal(self):
        for row in self.grid:
            if 0 in row:
                return False
            if len(row) != len(set(row)):
                return False
        return True

    def check_vertical(self):
        for i in range(COLS):
            column = []
            for j in range(ROWS):
                column.append(self.grid[j][i])
            if 0 in column:
                return False
            if len(column) != len(set(column)):
                return False
        return True

    def check_box(self):
        for box_number in range(0,9):
            box = []
            i = int(box_number / 3) * 3
            j = box_number % 3 * 3
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    box.append(self.grid[row][col])
            if 0 in box:
                return False
            if len(box) != len(set(box)):
                return False
        return True

    def check_win(self):
        return self.check_horizontal() and self.check_vertical() and self.check_box()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    self.selected_col = int(m_x / (TILE_SIZE + 1))
                    self.selected_row = int(m_y / (TILE_SIZE + 1))

                if event.type == pygame.KEYDOWN:
                    # Check key press on numbers
                    if event.key >= 49 and event.key <= 57 and self.fixed_grid[self.selected_row][self.selected_col] == 0:
                        self.grid[self.selected_row][self.selected_col] = int(chr(event.key))
                    elif event.key == pygame.K_RETURN:
                        if self.win:
                            self.__init__()
                        else:
                            self.grid = deepcopy(self.solved_grid)

                if event.type == pygame.QUIT:
                    running = False
            
            self.draw_grid()

            if self.check_win():
                if not self.win:
                    self.win_time = round(time.time() - self.win_time)
                self.draw_win_screen()
                self.win = True
                pass

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()