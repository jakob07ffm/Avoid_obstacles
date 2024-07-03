import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoid the Falling Blocks")

clock = pygame.time.Clock()

player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 10

obstacle_size = 50
obstacle_speed = 10
obstacle_list = []


def drop_obstacles(obstacle_list):
    delay = random.random()
    if len(obstacle_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - obstacle_size)
        y_pos = 0
        obstacle_list.append([x_pos, y_pos])

def draw_obstacles(obstacle_list):
    for obstacle_pos in obstacle_list:
        pygame.draw.rect(screen, BLUE, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

def update_obstacle_positions(obstacle_list, score):
    for idx, obstacle_pos in enumerate(obstacle_list):
        if obstacle_pos[1] >= 0 and obstacle_pos[1] < screen_height:
            obstacle_pos[1] += obstacle_speed
        else:
            obstacle_list.pop(idx)
            score += 1
    return score

def detect_collision(player_pos, obstacle_pos):
    p_x, p_y = player_pos
    o_x, o_y = obstacle_pos

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obstacle_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obstacle_size)):
            return True
    return False

def check_collisions(player_pos, obstacle_list):
    for obstacle_pos in obstacle_list:
        if detect_collision(player_pos, obstacle_pos):
            return True
    return False

game_over = False
score = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += player_speed

    screen.fill(BLACK)

    drop_obstacles(obstacle_list)
    score = update_obstacle_positions(obstacle_list, score)
    draw_obstacles(obstacle_list)

    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    if check_collisions(player_pos, obstacle_list):
        game_over = True
        break

    font = pygame.font.SysFont("monospace", 35)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

font = pygame.font.SysFont("monospace", 75)
game_over_text = font.render("Game Over", True, RED)
screen.blit(game_over_text, (screen_width / 2 - 200, screen_height / 2 - 50))
pygame.display.flip()

pygame.time.wait(2000)
pygame.quit()
sys.exit()
