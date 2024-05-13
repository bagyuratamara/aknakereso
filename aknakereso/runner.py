
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

pygame.init()

pygame.display.set_caption("Aknakereső")
screen = pygame.display.set_mode((600, 600))

rect1 = pygame.Rect(100, 270, 400, 130)
rect2 = pygame.Rect(100, 430, 400, 130)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                import aknakereso
            elif rect2.collidepoint(event.pos):
                from agent import main
                main()

        screen.fill((255, 255, 204))
        pygame.draw.rect(screen, (255, 196, 203), rect1)
        pygame.draw.rect(screen, (255, 196, 203), rect2)
        game_str = "AKNAKERSŐ"
        font = pygame.font.SysFont("comicsans", 90)
        game_text = font.render(game_str, True, (0,0,0))
        gtext_rect = game_text.get_rect()
        gtext_rect.center = (300,150)
        screen.blit(game_text,gtext_rect)
        game_str = "játék"
        font = pygame.font.SysFont("comicsans", 30)
        jatek_text = font.render(game_str, True, (0,0,0))
        jtext_rect = jatek_text.get_rect()
        jtext_rect.center = (300,335)
        screen.blit(jatek_text,jtext_rect)
        bot_str = "gép játszik"
        font = pygame.font.SysFont("comicsans", 30)
        bot_text = font.render(bot_str, True, (0,0,0))
        btext_rect = bot_text.get_rect()
        btext_rect.center = (300,495)
        screen.blit(bot_text,btext_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
