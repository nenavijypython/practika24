import pygame
import sys
import random
from diffic import *
from mode import choose_mode
from rounds import choose_rounds

pygame.init()
font_path = 'THUG____.TTF'
menu_font = pygame.font.Font(font_path, 36)
instruction_font = pygame.font.Font(None, 24)

# создание экрана и других основных настроек
screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Pong Game")
hit_sound = pygame.mixer.Sound('pong_sound.wav')  # звук ракеток
timer = pygame.time.Clock()
fr = 60

# определение цветов и начальных значений
background = (0, 0, 0)
block_color = (255, 255, 255)

paused = False
pongloop = True
game_over = False
winner_message = ""

# начальные позиции игроков и мяча
player1_place = 260
player2_place = 260
cpu_place = 260
ball_x = 290
ball_y = 290
pl1_direction = 0
pl2_direction = 0

# начальное направление движения мяча
ball_x_direction = random.choice([-1, 1])
ball_y_direction = random.choice([-1, 1])

font_large = pygame.font.Font(font_path, 36)
font_small = pygame.font.Font(font_path, 36)

mode = None
player1_score = 0
player2_score = 0
pl_speed_increment = 0.1  # увеличение скорости ракеток

# выбор сложности
selected_difficulty = DIFFICULTIES["standart"]
ball_speed = selected_difficulty["ball_speed"]
cpu_speed = selected_difficulty["cpu_speed"]
pl_speed = selected_difficulty["pl_speed"]

# обновление позиции cpu
def cpu_upd(cpu_place, ball_y, cpu_speed):
    # логика движения cpu в зависимости от положения мяча
    if cpu_place + 30 > ball_y + 10:
        cpu_place -= cpu_speed
    elif cpu_place + 30 < ball_y + 10:
        cpu_place += cpu_speed
    return cpu_place

# обновление позиции мяча
def ball_upd(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed):
    ball_x += ball_x_direction * ball_speed
    ball_y += ball_y_direction * ball_speed

    # отражение мяча от верхней и нижней границ
    if ball_y <= 0:
        ball_y = 0  # убеждаемся, что мяч не выходит за верхнюю границу
        ball_y_direction *= -1  # отражаем направление движения мяча

    if ball_y >= 580:  # учитываем размеры мяча
        ball_y = 580   # убеждаемся, что мяч не выходит за нижнюю границу
        ball_y_direction *= -1  # отражаем направление движения мяча

    return ball_x_direction, ball_y_direction, ball_x, ball_y

# проверка столкновений мяча с ракетками и увеличение скорости
def collusions_check(ball, player1, player2, ball_x_direction, ball_y_direction, ball_speed):
    global hit_sound
    global pl_speed, cpu_speed
    if ball.colliderect(player1):
        # мяч сталкивается с ракеткой игрока 1
        ball_x_direction = 1
        hit_sound.play()
        offset = (ball.centery - player1.centery) / 40
        ball_y_direction = offset
        ball_speed += 0.15
        pl_speed += pl_speed_increment
        if mode == "cpu":
            cpu_speed += pl_speed_increment
        else:
            cpu_speed += pl_speed_increment + 0.02
    elif ball.colliderect(player2):
        # мяч сталкивается с ракеткой игрока 2 или cpu
        ball_x_direction = -1
        hit_sound.play()
        offset = (ball.centery - player2.centery) / 40
        ball_y_direction = offset
        ball_speed += 0.1
        pl_speed += pl_speed_increment
        if mode == "cpu":
            cpu_speed += pl_speed_increment + 0.02
        else:
            cpu_speed += pl_speed_increment
    return ball_x_direction, ball_y_direction, ball_speed

# проверка конца игры
def check_the_end(ball_x):
    global player1_score, player2_score, game_over, winner_message
    if ball_x >= 600:
        # игрок 1 забивает гол
        player1_score += 1
        return True
    elif ball_x <= 0:
        # игрок 2 забивает гол
        player2_score += 1
        return True
    return False

# сброс позиций игроков и мяча
def reset_positions():
    global player1_place, player2_place, cpu_place, ball_x, ball_y, ball_x_direction, ball_y_direction, ball_speed, pl_speed, cpu_speed, paused
    player1_place = 260
    player2_place = 260
    cpu_place = 260
    ball_x = 290
    ball_y = 290
    ball_x_direction = random.choice([-1, 1])
    ball_y_direction = random.choice([-1, 1])
    ball_speed = selected_difficulty["ball_speed"]
    pl_speed = selected_difficulty["pl_speed"]
    cpu_speed = selected_difficulty["cpu_speed"]
    paused = True
    pygame.time.set_timer(pygame.USEREVENT, 2000)

# сброс очков
def reset_scores():
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0

# обработка событий
def handle_events():
    global pl1_direction, pl2_direction, paused, pongloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pongloop = False
        if event.type == pygame.KEYDOWN:  # работа с нажатыми кнопками
            if event.key == pygame.K_w:
                pl1_direction = -1
            if event.key == pygame.K_s:
                pl1_direction = 1
            if event.key == pygame.K_UP:
                pl2_direction = -1
            if event.key == pygame.K_DOWN:
                pl2_direction = 1
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_ESCAPE:
                pongloop = 0
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s]:
                pl1_direction = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                pl2_direction = 0
        if event.type == pygame.USEREVENT:
            paused = False

# выбор режима и количества раундов
mode = choose_mode(screen, font_large, font_small, background, block_color)
rounds = choose_rounds(screen, font_large, font_small, background, block_color)

# настройка сложности для режима cpu
if mode == "cpu":
    difficulty_settings = choose_difficulty(screen)
    ball_speed = difficulty_settings["ball_speed"]
    cpu_speed = difficulty_settings["cpu_speed"]

# основной игровой цикл
while pongloop:
    timer.tick(fr)
    screen.fill(background)
    player1 = pygame.draw.rect(screen, block_color, [5, player1_place, 20, 80])
    if mode == "cpu":
        player2 = pygame.draw.rect(screen, block_color, [575, cpu_place, 20, 80])
    else:
        player2 = pygame.draw.rect(screen, block_color, [575, player2_place, 20, 80])
    ball = pygame.draw.rect(screen, block_color, [ball_x, ball_y, 20, 20])

    handle_events()  # вызываем функцию для обработки событий

    if not paused:
        if not game_over:
            # обновление позиции игроков и мяча
            if mode == "cpu":
                cpu_place = cpu_upd(cpu_place, ball_y, cpu_speed)
            else:
                player2_place += pl_speed * pl2_direction
                if player2_place < 0:
                    player2_place = 0
                elif player2_place > 520:
                    player2_place = 520
            player1_place += pl_speed * pl1_direction
            if player1_place < 0:
                player1_place = 0
            elif player1_place > 520:
                player1_place = 520
            ball_x_direction, ball_y_direction, ball_x, ball_y = ball_upd(ball_x_direction, ball_y_direction, ball_x,
                                                                          ball_y, ball_speed)
        else:
            reset_positions()
            game_over = False

    if check_the_end(ball_x):
        reset_positions()
        # проверка на окончание игры по достижению количества раундов
        if player1_score >= rounds or player2_score >= rounds:
            if player1_score > player2_score:
                winner_message = "Player 1 wins!"
            elif player2_score > player1_score:
                winner_message = "Player 2 wins!"
            else:
                winner_message = "It's a tie!"
            reset_scores()
            game_over = True

    # отрисовка сообщения о победе, если игра окончена
    if game_over:
        winner_text = menu_font.render(winner_message, True, block_color)
        screen.blit(winner_text, (200, 200))
        pygame.display.flip()
        pygame.time.wait(3000)  # ждем 3 секунды
        pongloop = False  # выходим из игрового цикла

    score_text = menu_font.render(f"{player1_score} - {player2_score}", True, block_color)
    screen.blit(score_text, (280, 10))
    instructions_text = instruction_font.render("Space: Pause | Esc: Exit", True, block_color)
    screen.blit(instructions_text, (10, 10))
    ball_x_direction, ball_y_direction, ball_speed = collusions_check(ball, player1, player2, ball_x_direction,
                                                                      ball_y_direction, ball_speed)
    pygame.display.flip()

# завершение игры
pygame.quit()
sys.exit()
