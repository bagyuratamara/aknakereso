import sys
import random
import os
from collections import deque
import pygame
import numpy as np
from pygame.locals import *
import torch
import torch.optim as optim
import torch.nn.functional as F

from DQN_model import DQN 
from aknakereso_bot import MinesweeperGame

pygame.init()

class MinesweeperAgent:
    def __init__(self, state_dim, action_dim, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, gamma=0.9):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.memory = deque(maxlen=10000)
        self.model = DQN(state_dim, action_dim)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)
        state = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        self.model.eval()  
        
        try:
            for state, action, reward, next_state, done in minibatch:
                state = torch.FloatTensor(state).unsqueeze(0)
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                action = torch.LongTensor([action]).unsqueeze(1)
                reward = torch.FloatTensor([reward])
                done = torch.FloatTensor([done])

                q_values = self.model(state)
                next_q_values = self.model(next_state)
                max_next_q_values = torch.max(next_q_values, dim=1)[0]
                target_q_value = reward + (1 - done) * self.gamma * max_next_q_values

                current_q_values = q_values.gather(1, action)
                loss = F.mse_loss(current_q_values, target_q_value.unsqueeze(1))
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
        finally:
            self.model.train() 

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, path):
        save_dict = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'py_random_state': random.getstate(),
            'np_random_state': np.random.get_state()
        }
        torch.save(save_dict, path)

    def load(self, path):
        if os.path.exists(path) and os.path.getsize(path) > 0:
            checkpoint = torch.load(path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.epsilon = checkpoint['epsilon']
            random.setstate


def main():
    size = 10
    bomb_number = 10
    cell_size = 60
    screen_width = size * cell_size
    screen_height = size * cell_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minesweeper bot")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('britannic', 24)

    game = MinesweeperGame(size, bomb_number)
    agent = MinesweeperAgent(state_dim=100, action_dim=200)

    model_path = 'minesweeper_dqn.pth'
    if os.path.exists(model_path):
        agent.load(model_path)

    games = 100000
    total_wins = 0
    total_score = 0

    for g in range(1, games + 1):
        state = game.reset()
        done = False
        game_reward = 0
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            action = agent.act(state)
            next_state, reward, done = game.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            game_reward += reward

            draw_board(screen, game, font, cell_size)
            pygame.display.flip()
            clock.tick(30)

        total_score += game_reward
        if game.win:
            total_wins += 1
        average_score = total_score / g
        win_rate = total_wins / g * 100

        print(f"Játék: {g:<10} Pont: {game_reward:<10} Átlag pont: {average_score:.2f} Győzelem: {game.win:<10} Győzelmi arány: {win_rate:.2f}%")

        agent.replay(32)

        if g % 10 == 0:
            agent.save(model_path)
    agent.save(model_path)

def draw_board(screen, game, font, cell_size):
    screen.fill((255, 255, 204))
    for x in range(game.size):
        for y in range(game.size):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if game.revealed[x, y]:
                if game.board[x, y] == -1:
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 204), rect)
                    number = game.board[x, y]
                    if number > 0:
                        text = font.render(str(number), True, (0, 0, 255))
                        text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
                        screen.blit(text, text_rect)
            elif game.flags[x, y]:
                pygame.draw.rect(screen, (165, 42, 42), rect)
            else:
                pygame.draw.rect(screen, (255, 196, 203), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

if __name__ == "__main__":
    main()