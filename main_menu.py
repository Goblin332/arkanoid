import pygame, sys
from random import randrange as rnd  #модуль РАНДОМ. Для генератора диапазона случайных чисел



mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('game base')

#Добавляем музыку
pygame.mixer.music.load('8-Bit Misfits - Old Town Road.mp3')
pygame.mixer.music.play(-1, 0)

WIDTH, HEIGHT = 1200, 800 #Разрешение экрана/Ширина, Высота
fps = 60 #Кол-во кадров в секундку

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

font = pygame.font.SysFont(None, 20)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False


def main_menu():

    while True:
       #screen.fill((0, 0, 0))
        img_menu = pygame.image.load("formenu.jpg").convert()
        screen.blit(img_menu,(0, 0))
        draw_text('Arkanoid v 1.0', font, (255, 255, 255), screen, 20, 20)
        draw_text('made by DOLGANOFF', pygame.font.SysFont('Kino', 30),  (255, 255, 255), screen, WIDTH / 2 - 102, HEIGHT / 2 + 100)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 50, 400, 100)


        if button_1.collidepoint((mx, my)):
            if click:
                # main.run()
                run()


        pygame.draw.rect(screen, (255, 0, 0), button_1)
        draw_text('ИГРАТЬ', pygame.font.SysFont(None, 35, True), (255, 255, 255), screen, WIDTH / 2 - 50, HEIGHT / 2 - 13)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


#Задаю настройки платформы для мячика
platform_w = 330  #Ширина платформы
platform_h = 35 #Высота платформы
platform_speed = 13 #Скорость
platform = pygame.Rect(WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w, platform_h)
#Создадим Шарик
ball_rad = 20
ball_speed = 6
ball_rect = int(ball_rad * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
#Настройки блоков
block_set = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_set = [(rnd(30,256), rnd(30,256), rnd(30,256)) for i in range(10) for j in range(4)]

img = pygame.image.load("backdoor.jpg").convert()


def detect_colsn(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y)<10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_x < delta_y:
        dx = -dx
    return dx, dy

def run():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(img, (0, 0))
        #Отобразим Блоки
        [pygame.draw.rect(screen, color_set[color], block) for color, block in enumerate(block_set)] #Генератор рандомных цветов
        #Отобразим платформу
        pygame.draw.rect(screen, pygame.Color('red'), platform)
        #Отобразим Шарик
        pygame.draw.circle(screen, pygame.Color('green'),  ball.center, ball_rad)
        #Движение
        global dx, dy

        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        #Отражение Шарика слева
        if ball.centerx < ball_rad or ball.centerx  > WIDTH - ball_rad:
            dx = -dx
        #Отражение шаркиа по середине
        if ball.centery < ball_rad:
            dy = -dy
        #Сталкновение шарика и платформы
        if ball.colliderect(platform) and dy >0: #Возвращает истинное или ложное значенеи
            dx, dy = detect_colsn(dx, dy, ball, platform)
        #Сталкновение шарика с блоками
        hit = ball.collidelist(block_set)
        if hit != -1:
            hit_rect = block_set.pop(hit)#Удаление блока после столкновения
            hit_color = color_set.pop(hit)#Удаление цвета блока после столкновения
            dx , dy = detect_colsn(dx, dy, ball, hit_rect)
            #Анимация удара
            hit_rect.inflate_ip(ball.width / 3, ball.height / 3)
            pygame.draw.rect(screen, hit_color, hit_rect)
            global fps
            fps += 3 #Увеличиваем кол-во кадров после уничтожения каждого блока
            
        #Победа/Проигрыш
        if ball.bottom > HEIGHT:
            print("GAME OVER")
            ending((250, 250, 250), False)
        elif not len(block_set):
            print("YOU WIN ")
            ending((250, 250, 250), True)
        #Пишем управление
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and platform.left > 0:
            platform.left -= platform_speed
        if key[pygame.K_RIGHT] and platform.right < WIDTH:
            platform.right += platform_speed
    #Обновление экрана
        pygame.display.flip()
        mainClock.tick(fps)

def ending(bg_color,is_win):
    running = True
    while running:
        screen.fill((0, 0, 0))
        text =  "YOU WIN" if is_win else "YOU LOOSE"
        draw_text(text, pygame.font.SysFont(None, 60,True) , bg_color, screen, WIDTH / 2 - 110, HEIGHT/ 2 - 40)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                exit()
        pygame.display.update()
        mainClock.tick(60)



main_menu()
