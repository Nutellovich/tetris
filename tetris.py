# Подключение библиотек

import pygame
from copy import deepcopy
from random import choice, randrange
from os import path

# Инциализация переменных

width, height = (10, 20)
TILE = 45
GAME_RES = (width * TILE, height * TILE)
RES = (750, 940)
FPS = 50
grd = False
delay = 500
run = True
first = True

# Инициализация импортированных модулей PyGame

pygame.init()

# Инициализация игрового окна

sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)

# Таймер

clock = pygame.time.Clock()

# Сетка

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(width) for y in range(height)]

# Координаты квадратов всех фигур

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

# Инициализация фигур

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

# Игровое поле

field = [[0 for i in range(width)] for j in range(height)]

# Параметры анимации

anim_count, anim_speed, anim_limit = 0, 60, 2000

# определение картинок

bg = pygame.image.load('img/1.jpg').convert()
game_bg = pygame.image.load('img/2.jpg').convert()

# определение звука

snd_dir = path.join(path.dirname(__file__), 'snd')
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))

# определение шрифтов

# Основной
main_font = pygame.font.Font('font/20011.ttf', 65)
# Средний
font = pygame.font.Font('font/20011.ttf', 45)
# Малый
small_font = pygame.font.Font('font/20011.ttf', 35)

# Определение текста на экране

title_tetris = main_font.render('ТЕТРИС', True, pygame.Color('white'))
title_score = font.render('очки:', True, pygame.Color('white'))
title_record = font.render('рекорд:', True, pygame.Color('purple'))

# Текст на кнопках

title_button_exit = small_font.render('Выход', True, pygame.Color('purple'))
title_button_grid = small_font.render('Сетка', True, pygame.Color('purple'))
title_button_pause = small_font.render('Пауза', True, pygame.Color('purple'))
title_button_start = small_font.render('Старт', True, pygame.Color('purple'))

# Генерация рандомного цвета

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

# Объявляем переменные, которые отвечают за фигуры и очки

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# Определяем функции


def check_borders():
    """
    Проверка границ.
    В случае достажения конца поля проигрывается звук и возвращается True
    
    @ return: bool
    """
    if figure[i].x < 0 or figure[i].x > width - 1:
    
        return False
        
    elif figure[i].y > height - 1 or field[figure[i].y][figure[i].x]:
    
        shoot_sound.play()
        return False
        
    return True


def get_record():
    """
    Запросить рекорд.
    Если он был поставлен, то возвращается строку с рекордом, в противном случае - 0.
    
    @ return: pass
    """
    try:
    
        with open('record') as f:
        
            return f.readline()
            
    except FileNotFoundError:
    
        with open('record', 'w') as f:
        
            f.write('0')
    
    return


def set_record(record_, score_):
    """
    Записать рекорда.
    Рекорд обновляется, когда `record_` меньше `score_`.
    
    @ record_:string - текущий рекорд.
    @ score_ :string - счёт игрока в текущей игре.
    
    @ return: pass
    """
    
    rec = max(int(record_), score_)
    
    with open('record', 'w') as f:
    
        f.write(str(rec))
    
    return
    
# Game loop


while True:
    
    # Получить текущий рекорд
    record = get_record()
    
    dx, rotate = 0, False
    
    # Фон
    
    sc.blit(bg, (0, 0))
    
    # Сцена
    sc.blit(game_sc, (20, 20))
    
    # Фон сцены
    game_sc.blit(game_bg, (0, 0))

    # Кнопки

    start_button_exit = pygame.draw.rect(sc, (240, 240, 240), (620, 790, 120, 50))
    start_button_grid = pygame.draw.rect(sc, (240, 240, 240), (620, 860, 120, 50))
    start_button_pause = pygame.draw.rect(sc, (240, 240, 240), (490, 860, 120, 50))
    start_button_start = pygame.draw.rect(sc, (240, 240, 240), (490, 790, 120, 50))

    for i in range(lines):
    
        # Задержка для рендера
        
        pygame.time.wait(200)

    # Обработка игровых событий
    
    for event in pygame.event.get():
        """
        QUIT           - событие "Выход из игры"
        KEYDOWN        - событие "Клавиша нажата":
        
            K_LEFT  - Влево
            K_RIGHT - Вправо
            K_DOWN  - Вниз
            K_UP    - Вверх
            
        MOUSEBUTTONDOWN - событие "Мышь нажата":
        
        """
        if event.type == pygame.QUIT:
        
            exit()
            
        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_LEFT:
            
                dx = -1
                
            elif event.key == pygame.K_RIGHT:
            
                dx = 1
                
            elif event.key == pygame.K_DOWN:
            
                anim_limit = 100
                
            elif event.key == pygame.K_UP:
            
                rotate = True
                
        if event.type == pygame.MOUSEBUTTONDOWN:
        
            # Получить текущую позицию мыши
            
            mouse_pos = event.pos
            
            # Кнопка выхода
            
            if start_button_exit.collidepoint(mouse_pos):
            
                set_record(record, score)
                exit()
            
            # Кнопка начала игры
            
            if start_button_start.collidepoint(mouse_pos):
            
                run = True
            
            # Кнопка паузы
            
            if start_button_pause.collidepoint(mouse_pos):
            
                if run:
                    run = False
                else:
                    run = True
             
            # Кнопка вызова сетки
            
            if start_button_grid.collidepoint(mouse_pos):
            
                if grd:
                    grd = False
                else:
                    grd = True
    
    # Проверка состояния приложения (pause / play)
    
    if not run:
    
        continue

    # Отслеживание X

    figure_old = deepcopy(figure)
    
    for i in range(4):
    
        figure[i].x += dx
        if not check_borders():
        
            figure = deepcopy(figure_old)
            break

    # Отслеживание Y

    anim_count += anim_speed
    if anim_count > anim_limit:
    
        anim_count = 0
        figure_old = deepcopy(figure)
        
        for i in range(4):
        
            figure[i].y += 1
            if not check_borders():
            
                for j in range(4):
                
                    field[figure_old[j].y][figure_old[j].x] = color
                    
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    # Вращение фигур

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
    
        for i in range(4):
        
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
            
                figure = deepcopy(figure_old)
                break
                
    # Проверка линий

    line, lines = height - 1, 0
    for row in range(height - 1, -1, -1):
    
        count = 0
        for i in range(width):
        
            if field[row][i]:
                count += 1
                
            field[line][i] = field[row][i]
            
        if count < width:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Вычисление очков

    score += scores[lines]
    
    if score > 500:
    
        if score < 1500:
            FPS = 60
        elif score < 2000:
            FPS = 70
        elif score < 2500:
            FPS = 80
        else:
            FPS = 90

    # Прорисовка сетки при необходимости

    if grd:
    
        [pygame.draw.rect(game_sc, (180, 180, 180), i_rect, 1) for i_rect in grid]

    # Рисование фигур

    for i in range(4):
    
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

    # Прорисовка поля

    for y, raw in enumerate(field):
    
        for x, col in enumerate(raw):
        
            if col:
            
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    # Прорисовка следующей фигуры

    for i in range(4):
    
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    # Вывод текста и кнопкок

    sc.blit(title_tetris, (505, 40))
    sc.blit(title_score, (525, 450))
    sc.blit(font.render(str(score), True, pygame.Color('gold')), (550, 510))
    sc.blit(title_record, (525, 580))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 640))

    sc.blit(title_button_exit, (633, 801))
    sc.blit(title_button_grid, (635, 871))
    sc.blit(title_button_pause, (505, 871))
    sc.blit(title_button_start, (505, 801))

    # Вывод поля и с фигурами

    for i in range(width):
    
        if field[0][i]:
        
            set_record(record, score)
            field = [[0 for i in range(width)] for i in range(height)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            
            for i_rect in grid:
            
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)
                
    pygame.display.flip()
    
    if first:
    
        first = False
        run = False
        
    clock.tick(FPS)
