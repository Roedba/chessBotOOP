from functions import *
import pygame

pygame.init()
window = pygame.display.set_mode((600,600))

chessBoard = pygame.image.load("schachbrett.jpg")
window.blit(chessBoard, (0,0))

font = pygame.font.Font(None, 36)  # None uses default font, size 36

# Create class instances
piece = Piece()
bishop = Bishop()
knight = Knight()
rook = Rook()
queen = Queen()
king = King()
print(piece.testAllPositions(piece_pos, moveRight, oppositeMoveRight))
pygame.quit()
"""piece.draw(piece_pos, sq, window, images) # Draw starting position
legalMoves = legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piece_pos, legalMoves, enpassantPossibility) # get starting position legalMoves

running = True
while running:
    
        todo:
            use the pygame.display.update() method instead of pygame.display.flip(),
            to only update the neccesary parts of the board
            add error handling
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                lastMove = move
                move = moveRight + moveInput
                moveInput = ""

                if piece.move(move,move[0],piece_pos,legalMoves,movesSinceLastCapture, drawnConfigurations, oppositeMoveRight, moveRight):
                    window.blit(chessBoard, (0,0)) # Refresh board
                    piece.draw(piece_pos,sq,window,images)
                    
                    if moveRight == "w": # Swap turns
                        moveRight = "b"
                        oppositeMoveRight = "w"
                    elif moveRight == "b":
                        moveRight = "w"
                        oppositeMoveRight = "b"

                    legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piece_pos, legalMoves, enpassantPossibility)
                    print(f"Legal Moves: {legalMoves}")
            elif event.key == pygame.K_BACKSPACE:
                moveInput = moveInput[:-1]

            else:
                moveInput += event.unicode

            # Render and display the input text
            inputText = font.render(f"Input: {moveInput}", True, (255, 255, 255))  # White color
            pygame.draw.rect(window, (0, 0, 0), (10, 550, 600, 30))
            window.blit(inputText, (10, 550))  # Display near the bottom-left corner
            #implement gui, modify it when key is pressed

    pygame.display.flip()

    clock.tick(60)  # Limit to 60 frames per second
pygame.quit()"""