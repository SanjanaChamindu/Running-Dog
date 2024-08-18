import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 400))

start_time = 0


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render(f'score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(topleft=(5, 5))
    screen.blit(score_surface, score_rect)
    return current_time


def display_enemy(num):
    pass


# Set title
pygame.display.set_caption('Runner')

# Set frame rate
clock = pygame.time.Clock()

# Set text
test_font = pygame.font.Font(None, 30)

sky_surface = pygame.image.load('Graphics/sky.png').convert()
ground_surface = pygame.image.load('Graphics/land.png').convert()

name_surface = test_font.render('Dog Runner', False, (100, 100, 100))
name_rect = name_surface.get_rect(midtop=(400, 0))

game_message = test_font.render('Press space to run', False, (0, 0, 0))
game_message_rect = game_message.get_rect(midbottom=(400, 300))

# Load enemies
# snail_surface = pygame.image.load('Graphics/snails/snail1.png').convert_alpha()
# snail_rect = snail_surface.get_rect(bottomright=(800, 305))
# rock_surface = pygame.image.load('Graphics/snails/rock1.png').convert_alpha()

# obstacles = []
#
# for i in range(7):
#     obstacle_x = 900
#     obstacle_y = 300
#     surface = pygame.image.load(f'Graphics/snails/obstacle{i}.png')
#     obstacles.append(surface)
#
# current_obstacles = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)
obstacle_ys = [290, 300, 300]

obstacles = []
snails = []
bees = []
for snail in range(4):
    snail_surface = pygame.image.load(f'Graphics/snails/obstacle0.{snail}.png')
    snails.append(snail_surface)
obstacles.append(snails)

for bee in range(8):
    bee_surface = pygame.image.load(f'Graphics/snails/obstacle1.{bee}.png')
    bees.append(bee_surface)
obstacles.append(bees)

throne_surface = pygame.image.load('Graphics/snails/obstacle2.0.png')
obstacles.append([throne_surface])

# Load player
player_surface = []
player_rect = []
player_gravity = 0
for i in range(1, 13):
    player_surface.append(pygame.image.load(f'Graphics/Player/run{i}.png').convert_alpha())
    player_rect.append(player_surface[i-1].get_rect(midbottom=(100, 305)))

current_obstacles = []
obstacle_numbers = []
new_obstacle_ints = []
current_obstacles_rect = []
i, j = 0, 0
game_activate = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_activate:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect[j].collidepoint(event.pos):
                    player_gravity = -21

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player_rect[j].bottom >= 300:
                    player_gravity = -21

            if event.type == pygame.KEYUP:
                pass

            if event.type == obstacle_timer:
                new_obstacle_int = randint(0, 2)
                # print(new_obstacle_int)
                new_obstacle_ints.append(new_obstacle_int)
                obstacle_num = 0
                obstacle_numbers.append(obstacle_num)
                current_obstacles.append(obstacles[new_obstacle_int][obstacle_num])
                current_obstacles_rect.append(obstacles[new_obstacle_int][obstacle_num].get_rect(
                    bottomright=(randint(900, 1200), obstacle_ys[new_obstacle_int])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_activate = True
                    # snail_rect.left = 800
                    start_time = pygame.time.get_ticks()

    if game_activate:

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # pygame.draw.rect(screen, '#c0e8ec', text_rect)
        # pygame.draw.rect(screen, '#c0e8ec', text_rect, 6, 20)
        # screen.blit(text_surface, text_rect)

        # pygame.draw.line(screen, 'Gold', (0, 0), pygame.mouse.get_pos(), 10)
        # pygame.draw.ellipse(screen, 'Blue', pygame.Rect(50, 200, 100, 100))

        # l = len(current_obstacles)
        # for item in range(l):
        #     current_obstacles_rect[item].x -= 8
        #
        #     if player_rect[j].colliderect(current_obstacles_rect[item]):
        #         game_activate = False
        #         current_obstacles_rect = []
        #         current_obstacles = []
        #         break
        #
        #     screen.blit(current_obstacles[item], current_obstacles_rect[item])
        #
        #     if current_obstacles_rect[item].x <= -64:
        #         current_obstacles_rect[item] = 0
        #         current_obstacles[item] = 0

        obstacle_length = len(current_obstacles_rect)
        # print(obstacle_length)
        # print(len(current_obstacles_rect))
        for obs in range(obstacle_length):
            if player_rect[j].colliderect(current_obstacles_rect[obs]):
                game_activate = False
                current_obstacles_rect = []
                current_obstacles = []
                obstacle_numbers = []
                obstacle_length = []
                break

            current_obstacles_rect[obs].x -= 8
            screen.blit(current_obstacles[obs], current_obstacles_rect[obs])

            if obstacle_numbers[obs] >= len(obstacles[new_obstacle_ints[obs]])-1:
                obstacle_numbers[obs] = 0
            else:
                obstacle_numbers[obs] += 0.1

            current_obstacles[obs] = obstacles[new_obstacle_ints[obs]][round(obstacle_numbers[obs])]

            if current_obstacles_rect[obs].x <= -64:
                current_obstacles_rect[obs] = 0
                current_obstacles[obs] = 0
                new_obstacle_ints[obs] = 99
                obstacle_numbers[obs] = 99

        current_obstacles_rect = [item for item in current_obstacles_rect if item != 0]
        current_obstacles = [items for items in current_obstacles if items != 0]
        new_obstacle_ints = [items for items in new_obstacle_ints if items != 99]
        obstacle_numbers = [items for items in obstacle_numbers if items != 99]

        player_gravity += 1
        player_rect[j].y += player_gravity
        if player_rect[j].bottom >= 300:
            player_rect[j].bottom = 300
        elif player_rect[j].bottom < 300:
            player_rect[11].y = player_rect[j].y
            j = 11

        for k in range(12):
            player_rect[k].y = player_rect[j].y
        # screen.blit(snail_surface, snail_rect)
        screen.blit(player_surface[j], player_rect[j])
        i += 0.3
        j = round(i)
        if j == 12:
            i, j = 0, 0

        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # snail_rect.x -= 8

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('Jump')

        # if player_rect[j].colliderect(snail_rect):
        #     game_activate = False

    else:
        screen.blit(name_surface, name_rect)
        screen.blit(game_message, game_message_rect)
        final_surface = test_font.render(f'Final score:{score}', False, (64, 64, 64))
        final_rect = final_surface.get_rect(midtop=(400, 100))
        screen.blit(final_surface, final_rect)

    # Update screen
    pygame.display.update()
    # Limit the frame rate
    clock.tick(60)

