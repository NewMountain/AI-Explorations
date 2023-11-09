import random

import numpy as np
import pygame
import pygame.surfarray

# Initialize Pygame
pygame.init()

MAX_SCORE = 15

# Screen dimensions
WIDTH, HEIGHT = 640, 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 70
paddle_speed = 7

# Ball properties
BALL_WIDTH, BALL_HEIGHT = 10, 10

# Score variables
player_score = 0
opponent_score = 0

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def ball_restart():
    ball = pygame.Rect(
        WIDTH // 2 - BALL_WIDTH // 2,
        HEIGHT // 2 - BALL_HEIGHT // 2,
        BALL_WIDTH,
        BALL_HEIGHT,
    )
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = 5 * random.choice((1, -1))
    return ball, ball_speed_x, ball_speed_y


def reset_game():
    global player_score, opponent_score
    player_paddle = pygame.Rect(
        WIDTH - PADDLE_WIDTH - 10,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    )
    opponent_paddle = pygame.Rect(
        10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
    )
    ball, ball_speed_x, ball_speed_y = ball_restart()
    player_score = 0
    opponent_score = 0
    return (
        player_paddle,
        opponent_paddle,
        ball,
        ball_speed_x,
        ball_speed_y,
        player_score,
        opponent_score,
    )


def step_game(player_paddle, opponent_paddle, ball, ball_speed_x, ball_speed_y, action):
    global player_score, opponent_score
    # print(f"Player score {player_score}, opponent score: {opponent_score}")

    # Apply the action (move AI paddle)
    if action == 1 and opponent_paddle.top > 0:
        opponent_paddle.y -= paddle_speed
    elif action == 2 and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += paddle_speed

    # Update ball position
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    paddle_hit = 0
    if ball.colliderect(player_paddle):
        ball_speed_x *= -1
        paddle_hit = 1
    elif ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Update scores and check if game should end
    done = False
    if ball.left <= 0:
        opponent_score += 1
        if opponent_score >= MAX_SCORE:  # End game if opponent reaches 10 points
            done = True
        ball, ball_speed_x, ball_speed_y = ball_restart()
    elif ball.right >= WIDTH:
        player_score += 1
        if player_score >= MAX_SCORE:  # End game if player reaches 10 points
            done = True
        ball, ball_speed_x, ball_speed_y = ball_restart()

    # Capture the frame
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.transpose(frame, (1, 0, 2))  # Transpose it to proper format

    return (
        player_paddle,
        opponent_paddle,
        ball,
        ball_speed_x,
        ball_speed_y,
        player_score,
        opponent_score,
        done,
        paddle_hit,
        frame,
    )


if __name__ == "__main__":
    # For human use
    player_paddle = pygame.Rect(
        WIDTH - PADDLE_WIDTH - 10,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    )
    opponent_paddle = pygame.Rect(
        10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
    )
    ball, ball_speed_x, ball_speed_y = ball_restart()

    # Game loop for testing step_game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example player action (e.g., 0 = stay, 1 = up, 2 = down)
        player_action = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_action = 1
        elif keys[pygame.K_DOWN]:
            player_action = 2

        # Update the game state
        (
            player_paddle,
            opponent_paddle,
            ball,
            ball_speed_x,
            ball_speed_y,
            player_score,
            opponent_score,
            done,
            paddle_hit,
            frame,
        ) = step_game(
            player_paddle,
            opponent_paddle,
            ball,
            ball_speed_x,
            ball_speed_y,
            player_action,
        )

        print(f"Player Score: {player_score}. Opponent Score: {opponent_score}")

        if done:
            break

        # Update the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.display.flip()

    pygame.quit()
