import pygame

black = (0,0,0)
white = (255,255,225)

red = (255,0,0)
WIDTH = 20
HEIGHT = 20
MARGIN = 5
grid = []
for row in range(3):
    grid.append([])
    for columns in range(3):
        grid[row].append(0)
grid[0][0] = 1

pygame.init()

window_size = [255,255]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Grid")
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT