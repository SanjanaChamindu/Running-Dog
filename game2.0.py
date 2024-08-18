import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 400))

start_time = 0


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = score_font.render(f'score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(topleft=(5, 5))
    screen.blit(score_surface, score_rect)
    return current_time


def display_enemy(num):

    current_obstacles_rect[num].x -= 8
    screen.blit(current_obstacles[num], current_obstacles_rect[num])

    if obstacle_numbers[num] >= len(obstacles[new_obstacle_ints[num]]) - 1:
        obstacle_numbers[num] = 0
    else:
        obstacle_numbers[num] += 0.3

    current_obstacles[num] = obstacles[new_obstacle_ints[num]][round(obstacle_numbers[num])]

    if current_obstacles_rect[num].x <= -64:
        current_obstacles_rect[num] = 0
        current_obstacles[num] = 0
        new_obstacle_ints[num] = 99
        obstacle_numbers[num] = 99

    return current_obstacles_rect, current_obstacles, new_obstacle_ints, obstacle_numbers


def is_collide(player_j, enemy_obs):
    if current_obstacles_rect[enemy_obs] != 0 and player_rect[player_j].colliderect(current_obstacles_rect[enemy_obs]):
        return False, True
    else:
        return True, False


# Set title
pygame.display.set_caption('Runner')

# Set frame rate
clock = pygame.time.Clock()

# Set text
test_font = pygame.font.Font('Font/uchiyama.ttf', 30)
score_font = pygame.font.Font('Font/Sabatica-regular.ttf', 20)

sky_surface = pygame.image.load('Graphics/sky.png').convert()
ground_surface = pygame.image.load('Graphics/land.png').convert()

name_surface = test_font.render('Dog Runner', False, (100, 100, 100))
name_rect = name_surface.get_rect(midtop=(400, 0))

game_message = test_font.render('Press space to run', False, (0, 0, 0))
game_message_rect = game_message.get_rect(midbottom=(400, 300))

# Load enemies
start_timer = 1800
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, start_timer)
obstacle_ys = [300, 295, 300, 300, 300, 300]

obstacles = []
bird1 = []
bird2 = []
kangaroo = []
lion = []
cat1 = []
bear = []


for bird in range(18):
    bird_surface = pygame.image.load(f'Graphics/Obstacles/bird1/obstacle.0.{bird}.png').convert_alpha()
    bird1.append(bird_surface)
obstacles.append(bird1)

for bird in range(12):
    bird_surface = pygame.image.load(f'Graphics/Obstacles/bird2/bird2.{bird}.png').convert_alpha()
    bird2.append(bird_surface)
obstacles.append(bird2)

for kang in range(12):
    kangaroo_surface = pygame.image.load(f'Graphics/Obstacles/kangaroo/kang{kang}.png').convert_alpha()
    kangaroo.append(kangaroo_surface)
obstacles.append(kangaroo)

for lions in range(12):
    lion_surface = pygame.image.load(f'Graphics/Obstacles/lion/lion.{lions}.png').convert_alpha()
    lion.append(lion_surface)
obstacles.append(lion)

for bears in range(12):
    bear_surface = pygame.image.load(f'Graphics/Obstacles/bear/bear0.{bears}.png').convert_alpha()
    bear.append(bear_surface)
obstacles.append(bear)

for cat in range(12):
    cat_surface = pygame.image.load(f'Graphics/Obstacles/cat1/cat.{cat}.png').convert_alpha()
    cat1.append(cat_surface)
obstacles.append(cat1)


# Load player
player_surface = []
player_rect = []
player_gravity = 0
for i in range(12):
    player_surface.append(pygame.image.load(f'Graphics/Player/dog{i}.png').convert_alpha())
    player_rect.append(player_surface[i-1].get_rect(midbottom=(100, 305)))


current_obstacles = []
obstacle_numbers = []
new_obstacle_ints = []
current_obstacles_rect = []
i, j = 0, 0
game_activate = False
game_over = False
ecs_time = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_activate:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect[j].collidepoint(event.pos):
                    player_gravity = -10

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player_rect[j].bottom >= 290:
                    player_gravity = -7

                if event.key == pygame.K_ESCAPE:
                    game_activate = False
                    ecs_time = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                pass

            if event.type == obstacle_timer:
                new_obstacle_int = randint(0, 5)
                new_obstacle_ints.append(new_obstacle_int)
                obstacle_num = 0
                obstacle_numbers.append(obstacle_num)
                current_obstacles.append(obstacles[new_obstacle_int][obstacle_num])
                current_obstacles_rect.append(obstacles[new_obstacle_int][obstacle_num].get_rect(
                    bottomright=(randint(900, 1200), obstacle_ys[new_obstacle_int])))
                if not start_timer <= 800:
                    start_timer -= 2
                    pygame.time.set_timer(obstacle_timer, start_timer)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_activate and not game_over:
                        start_time += pygame.time.get_ticks() - ecs_time
                    game_activate = True
                    game_over = False

    if game_activate and not game_over:

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        obstacle_length = len(current_obstacles_rect)
        for obs in range(obstacle_length):
            current_obstacles_rect, current_obstacles, new_obstacle_ints, obstacle_numbers = display_enemy(obs)
            game_activate, game_over = is_collide(j, obs)

            if not game_activate:
                break

        current_obstacles_rect = [item for item in current_obstacles_rect if item != 0]
        current_obstacles = [items for items in current_obstacles if items != 0]
        new_obstacle_ints = [items for items in new_obstacle_ints if items != 99]
        obstacle_numbers = [items for items in obstacle_numbers if items != 99]

        player_gravity += 0.3
        player_rect[j].y += player_gravity
        if player_rect[j].bottom >= 300:
            player_rect[j].bottom = 300
        elif player_rect[j].bottom < 300:
            player_rect[11].y = player_rect[j].y
            j = 11

        for k in range(12):
            player_rect[k].y = player_rect[j].y

        screen.blit(player_surface[j], player_rect[j])
        i += 0.4
        j = round(i)
        if j == 12:
            i, j = 0, 0

    elif game_over:
        start_timer = 1800
        start_time = pygame.time.get_ticks()

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        screen.blit(name_surface, name_rect)
        screen.blit(game_message, game_message_rect)

        current_obstacles = []
        obstacle_numbers = []
        new_obstacle_ints = []
        current_obstacles_rect = []

        score_file = open('Score/High Score.txt', 'r')
        high_score = int(score_file.read())
        score_file.close()
        if high_score <= score:
            final_text = 'Congratulations! New high score'
            score_file = open('Score/High Score.txt', 'w')
            score_file.write(str(score))
            score_file.close()
        else:
            final_text = f'High score: {high_score}'

        final_surface = score_font.render(f'Final score: {score}', False, (64, 64, 64))
        final_rect = final_surface.get_rect(midtop=(400, 100))
        screen.blit(final_surface, final_rect)

        high_score_surface = score_font.render(final_text, False, (64, 64, 64))
        final_rect = high_score_surface.get_rect(midtop=(400, 200))
        screen.blit(high_score_surface, final_rect)
    elif not game_activate and not game_over:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        screen.blit(name_surface, name_rect)
        screen.blit(game_message, game_message_rect)

    # Update screen
    pygame.display.update()
    # Limit the frame rate
    clock.tick(60)
