from functions import *
import pygame
import time
import cProfile
import pstats
with cProfile.Profile() as profile:
    pygame.init()
    window = pygame.display.set_mode((600,600))

    chessBoard = pygame.image.load("schachbrett.jpg")
    window.blit(chessBoard, (0,0))

    font = pygame.font.Font(None, 36)  # None uses default font, size 36

    piece.draw(piecePos, sq, window, images) # Draw starting position
    legalMoves = legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility) # get starting position legalMoves

    running = True
    while running:
        
        """ todo:
                use the pygame.display.update() method instead of pygame.display.flip(),
                to only update the neccesary parts of the board
                add error handling
                for depth of 4 the engine needs 2-4 minutes, depth of 2 is a minimum for correct evaluation though, depth of 3 is the goal
                i need to somehow speed up the program 100x
                depth of 1 took 0.24305462837219238 seconds in start pos
                depth of 2 took 13.085906028747559 seconds in start pos
                when making a second move, the program takes 108.803866147995 seconds at a depth of 2. At depth of 1 the max time is around 1.5 seconds
                for some reason, the program slows down exponentially with the depth when it makes the second move
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    lastMove = move
                    move = moveRight + moveInput
                    moveInput = ""
                    if moveRight == "b":
                        if piece.move(move,move[0],piecePos,legalMoves,movesSinceLastCapture, drawnConfigurations, oppositeMoveRight, moveRight):
                            window.blit(chessBoard, (0,0)) # Refresh board
                            piece.draw(piecePos,sq,window,images)
                            
                            if moveRight == "w": # Swap turns
                                moveRight = "b"
                                oppositeMoveRight = "w"
                            elif moveRight == "b":
                                moveRight = "w"
                                oppositeMoveRight = "b"

                            legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility)
                            if piece.isCheckmate(legalMoves, piecePos, oppositeMoveRight):
                                print("Checkmate")
                                #running = False

                            if piece.isStalemate(legalMoves, piecePos, oppositeMoveRight):
                                print("Stalemate")
                                #running = False
                elif event.key == pygame.K_BACKSPACE:
                    moveInput = moveInput[:-1]

                else:
                    moveInput += event.unicode

                # Render and display the input text
                inputText = font.render(f"Input: {moveInput}", True, (255, 255, 255))  # White color
                pygame.draw.rect(window, (0, 0, 0), (10, 550, 600, 30))
                window.blit(inputText, (10, 550))  # Display near the bottom-left corner
                #implement gui, modify it when key is pressed
        if moveRight == "w":
            startTime = time.time()
            move = chessbot.chessBot(piecePos, moveRight, oppositeMoveRight, enpassantPossibility, 4)[0]
            print(time.time()-startTime)
            if piece.move(move,move[0],piecePos,legalMoves,movesSinceLastCapture, drawnConfigurations, oppositeMoveRight, moveRight):
                window.blit(chessBoard, (0,0)) # Refresh board
                piece.draw(piecePos,sq,window,images)
                
                if moveRight == "w": # Swap turns
                    moveRight = "b"
                    oppositeMoveRight = "w"
                elif moveRight == "b":
                    moveRight = "w"
                    oppositeMoveRight = "b"

                legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility)
                if piece.isCheckmate(legalMoves, piecePos, oppositeMoveRight):
                    print("Checkmate")
                    #running = False

                if piece.isStalemate(legalMoves, piecePos, oppositeMoveRight):
                    print("Stalemate")
                    #running = False
        pygame.display.flip()

        clock.tick(60)  # Limit to 60 frames per second
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
    results.dump_stats("results.prof")