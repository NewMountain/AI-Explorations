from collections import deque

import cv2
import game
import gym
import numpy as np
import pygame
from gym import spaces
from stable_baselines3 import PPO


class CustomPongEnv(gym.Env):
    def __init__(self):
        super(CustomPongEnv, self).__init__()
        self.action_space = spaces.Discrete(3)  # Actions: 0 = Stay, 1 = Up, 2 = Down

        self.frame_stack_size = 3  # Number of frames to stack

        self.observation_space = spaces.Box(
            low=0, high=255, shape=(80, 80, 3 * self.frame_stack_size), dtype=np.uint8
        )
        self.frames = deque(maxlen=self.frame_stack_size)  # Use deque to store frames

        self.player_score = 0
        self.opponent_score = 0

        pygame.init()
        self.screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT))
        pygame.display.set_caption("Pong")

        # Initialize the game state
        self.reset()

    def process_frame(self, frame):
        # Resize the frame to a smaller size, e.g., (80, 80)
        frame = cv2.resize(frame, (80, 80), interpolation=cv2.INTER_AREA)
        return frame

    def step(self, action):
        # Use step_game from game.py to update the game state
        (
            self.player_paddle,
            self.opponent_paddle,
            self.ball,
            self.ball_speed_x,
            self.ball_speed_y,
            player_score,
            opponent_score,
            done,
            paddle_hit,
            frame,
        ) = game.step_game(
            self.player_paddle,
            self.opponent_paddle,
            self.ball,
            self.ball_speed_x,
            self.ball_speed_y,
            action,
        )

        # Calculate reward and check if episode is done
        if paddle_hit:
            # We really want our bot to learn to hit the ball
            # at this point, that's more valuable than the point itself
            reward = 10

        if player_score > self.player_score:
            reward = 1
            self.player_score = player_score
        elif opponent_score > self.opponent_score:
            reward = -1
            self.opponent_score = opponent_score
        else:
            reward = 0

        frame = self.process_frame(frame)
        self.frames.append(frame)
        stacked_frames = np.concatenate(self.frames, axis=-1)  # Stack frames
        return stacked_frames, reward, done, {}

    def reset(self):
        # Reset the game to its initial state
        (
            self.player_paddle,
            self.opponent_paddle,
            self.ball,
            self.ball_speed_x,
            self.ball_speed_y,
            self.player_score,
            self.opponent_score,
        ) = game.reset_game()

        # Capture the initial frame
        _, _, _, _, _, _, _, _, _, frame = game.step_game(
            self.player_paddle,
            self.opponent_paddle,
            self.ball,
            self.ball_speed_x,
            self.ball_speed_y,
            0,  # Assuming '0' is the action for 'stay'
        )
        frame = self.process_frame(frame)

        self.frames.clear()
        for _ in range(self.frame_stack_size):
            self.frames.append(frame)  # Initialize with repeated frames

        stacked_frames = np.concatenate(self.frames, axis=-1)  # Stack frames
        return stacked_frames

    def render(self, mode="human"):
        if mode == "human":
            # Check if the screen is initialized
            if self.screen is None:
                self.screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT))

            # Draw the game objects
            self.screen.fill(game.BLACK)
            pygame.draw.rect(self.screen, game.WHITE, self.player_paddle)
            pygame.draw.rect(self.screen, game.WHITE, self.opponent_paddle)
            pygame.draw.ellipse(self.screen, game.WHITE, self.ball)

            # Update the display
            pygame.display.flip()

    def close(self):
        # Optional: close resources if any
        pass


# Initialize the Gym environment
env = CustomPongEnv()

# Initialize the model
model = PPO("CnnPolicy", env, verbose=1)


for i in range(10):
    model.learn(total_timesteps=10_000)
    obs = env.reset()
    for _ in range(2_500):  # Render 1000 steps of the trained model
        action, _states = model.predict(obs, deterministic=True)
        # print(f"Action predicted: {action}")
        obs, rewards, dones, info = env.step(action)
        env.render()
