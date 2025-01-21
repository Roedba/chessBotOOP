from definitions import *
from functions import *
import pygame

pygame.init()
window = pygame.display.set_mode((600,600))

chessoard = pygame.image.load("schachbrett.jpg")
window.blit(chessoard, (0,0))
piece = Piece()
piece.draw(piece_pos,sq,window,images)
running = True
while running:
    """
        todo:
            implement gui so the user can see the inputMove
            call draw function after move function is called (not every frame)
            call move function when return is pressed
            use the pygame.display.update() method instead of pygame.display.flip(),
            to only update the neccesary parts of the board
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and moveRight + moveInput in legalMoves:
                move = moveRight + moveInput
                moveInput = ""

            elif event.key == pygame.K_BACKSPACE:
                moveInput = moveInput[:-1]

            else:
                moveInput += event.unicode
            #implement gui, modify it when key is pressed

    pygame.display.flip()

    clock.tick(60)  # Limit to 60 frames per second