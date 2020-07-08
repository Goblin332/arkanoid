import pygame #Модуль пайгем на котором и будет создаватсья игра
from random import randrange as rnd  #модуль РАНДОМ. Для генератора диапазона случайных чисел

WIDTH, HEIGHT = 1200, 800 #Разрешение экрана/Ширина, Высота
fps = 60 #Кол-во кадров в секундку


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


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
#Здесь картинка для фона
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    #Отобразим Блоки
    [pygame.draw.rect(sc, color_set[color], block) for color, block in enumerate(block_set)] #Генератор рандомных цветов
    #Отобразим платформу
    pygame.draw.rect(sc, pygame.Color('red'), platform)
    #Отобразим Шарик
    pygame.draw.circle(sc, pygame.Color('green'),  ball.center, ball_rad)
    #Движение шарика
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    #Отражение Шарика слева
    if ball.centerx < ball_rad or ball.centerx  > WIDTH - ball_rad:
        dx= -dx
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
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 3 #Увеличиваем кол-во кадров после уничтожения каждого блока
    #Победа/Проигрыш
    if ball.bottom > HEIGHT:
        print("GAME OVER")
        exit()
    elif not len(block_set):
        print("YOU WIN ")
        exit()
    #Пишем управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed
#Обновление экрана
    pygame.display.flip()
    clock.tick(fps)