import pygame
from definitions import *
import random
"""
todo:

    1.Objectives:
        implement check
        implement checkmate and stalemate

    Draw rules: LOGIC DONE, only need to implement drawing mechanism
        3 move repetition -- add dictionary that tracks all positions and has a counter and if theres the same position increases the counter by one. once it reaches three its a draw
        50 move rule -- track when the last capture happened, if its 50 moves ago its a draw
        insufficient material to checkmate -- add a list of piece configurations that are drawn and add a list of all pieces that are on the board, then check if the pieces on the board are in the list of drawn games

    2.Extras:
        option to take back moves -- create a dict that tracks the last position, then create a clickable button that changes the current piece_pos to the last piece_pos
        option to restart game -- create a dict that holds the starting position, then add a clickable button that changes the current piece_pos to the starting piece_pos
        option to flip the board -- add a variable called current_sq that holds square coordinates, create a sq that is reversed and then switch to that sq
        add a start menu where you can choose your starting color
        add time control to the start menu -- let a timer run down, when a player moves the other timer starts going down
        add number identifier to piece images

    FIX:
        getLegalMoves iterates over all pieces and not only the piece it gets the legalMoves for
"""
class Piece:
    def __init__(self):
        pass

    def move(self,move,pieceColor,piecePos,legalMoves,movesSinceLastCapture,drawnConfigurations, oppositeMoveRight, moveRight):
        piece = move[0:3]
        destination = move[3:5]
        # Destination like a3 and piece like wR1
        if move in legalMoves:
            if move == "w0-0":
                piecePos["wK1"] = "g1"
                piecePos["wR2"] = "f1"

            elif move == "w0-0-0":
                piecePos["wK1"] = "c1"
                piecePos["wR1"] = "d1"
            
            elif move == "b0-0":
                piecePos["bK1"] = "g8"
                piecePos["bR2"] = "f8"

            elif move == "b0-0-0":
                piecePos["bK1"] = "c8"
                piecePos["bR1"] = "d8"

            elif move[1] == "P" and len(move) == 6:
                del piecePos[move[0:3]]

                piecePos[f"{move[0]}{move[5]}{pieceCount[move[0] + move[5]] + 1}"] = move[3:5] #add piece to piece pos after promotion
                pieceCount[move[0:2]] += 1
            
            elif move[1] == "P" and len(move) > 6:
                if move[5:8] == "e.p":
                    column = "12345678"
                    enpassantTargetSquare = destination[0] + column[column.index(destination[1])-1]
                    enpassantTarget =  next((key for key, value in piecePos.items() if value == enpassantTargetSquare), None)
                    del piecePos[enpassantTarget]
                    piecePos[piece] = destination
            if move[1] == "P":
                if move[4] in ("4", "5") and piecePos[piece][1] in ("2", "7"): # Python doesnt use "or" like a human, not my fault stupid. Waste of my time
                    enpassantPossibility[0] = "possible"
                    enpassantPossibility[1] = move
                else:
                    enpassantPossibility[0] = "notPossible"
                    enpassantPossibility[1] = None
            else:
                enpassantPossibility[0] = "notPossible"
                enpassantPossibility[1] = None

            piecePos[piece] = destination # If the piecePos dict is modified the passed dict is also modified(passing by reference)
            pieceMoveCount[move[0:3]] += 1
            for loopPiece,position in piecePos.items(): # delete piece if taken
                if position == destination and loopPiece != piece and loopPiece[0] != piece[0]:
                    del piecePos[loopPiece]
                    pieceCount[move[0:2]] -= 1
                    piecePosKey = frozenset(piecePos.items())
                    if piecePosKey in piecePosDict:
                        piecePosDict[piecePosKey] += 1
                    else:
                        piecePosDict[piecePosKey] = 1
                    movesSinceLastCapture[0] = 0
                    for drawnConfiguration in drawnConfigurations:
                        if set(drawnConfiguration.keys()) == set(piecePos.keys()): #convert dict keys to set so order doesnt matter
                            # Implement drawing logic here
                            pass
                    return True
                
            """isCheckmate = self.isCheckmate(piecePos, moveRight, oppositeMoveRight)
            if isCheckmate == "2":
                #Implement Checkmate logic here
                print("CHECKMATE")
                pass
            if isCheckmate == "1":
                #Implement Stalemate logic here
                print("STALEMATE")
                pass"""

            piecePosKey = frozenset(piecePos.items()) # Track how often positions are repeated.
            if piecePosKey in piecePosDict:
                piecePosDict[piecePosKey] += 1
                if piecePosDict[piecePosKey] == 3:
                    # Implement drawing logic
                    pass
            else:
                piecePosDict[piecePosKey] = 1
            movesSinceLastCapture[0] += 1
            if movesSinceLastCapture[0] >= 100:
                # Implement drawing logic
                pass
            return True

        else:
            print(f"Illegal move: {piece} to {destination}")
            return False
            # If not a legal move, return false

    def draw(self,piecePos,squareCoords,chessBoard,images):
        # Specific function
        for piece in piecePos:
            extractedCoords = squareCoords[piecePos[piece]].split("|")
            pieceImage = images[piece]
            chessBoard.blit(pieceImage,(int(extractedCoords[0]),int(extractedCoords[1])))

    def getLegalMoves(self,moveRight,piecePos,board):
        # Basic function structure, raise error if not implemented in subclass
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def isCheck(self,piecePos, isCapture, move,oppositeMoveRight):
        # Check if King is in Check after a move
        if move == "bP5f5":
            print(move)
        if move != None:
            newPiecePos = self.simulateMove(move,piecePos, isCapture)
        else:
            newPiecePos = piecePos.copy()
            if oppositeMoveRight == "w":
                move = "b"
            else:
                move = "w"
        kingPos = newPiecePos[f"{move[0]}K1"]
        isCheckLegalMoves = getAllIsCheckLegalMoves(newPiecePos, oppositeMoveRight, legalMoves)
        for isCheckMove in isCheckLegalMoves:
            if isCheckMove[3:5] == kingPos: # and isCheckMove[0:3] in newPiecePos.items()
                if isCheckMove[0:3] in newPiecePos:
                    return True
        return False
    
    def simulateMove(self,move, piecePos, isCapture):
        newPiecePos = piecePos.copy()  # Create a copy of piecePos
        if move =="w0-0":
            piecePos["wK1"] = "g1"
            piecePos["wR2"] = "f1"
            return newPiecePos
        if move =="w0-0-0":
            piecePos["wK1"] = "c1"
            piecePos["wR1"] = "d1"
            return newPiecePos
        if move =="b0-0":
            piecePos["bK1"] = "g8"
            piecePos["bR2"] = "f8"
            return newPiecePos
        if move =="b0-0-0":
            piecePos["bK1"] = "c8"
            piecePos["bR1"] = "d8"
            return newPiecePos
        piece = move[:3]  # Extract the piece (e.g., "wP1")
        destination = move[3:5]  # Extract the destination (e.g., "e4")

        # Update the piece's position
        newPiecePos[piece] = destination

        # Handle captures
        for p, pos in list(newPiecePos.items()):
            if pos == destination and p != piece:
                if move[1] == "P" and isCapture == True:
                    del newPiecePos[p]
                elif move[1] != "P":
                    del newPiecePos[p]  # Remove the captured piece
                    continue
        return newPiecePos

    def isCheckmate(self, legalMoves, piecePos, oppositeMoveRight):
        if not legalMoves:
            if self.isCheck(piecePos, True, None, oppositeMoveRight):
                return True
        return False
    
    def isStalemate(self, legalMoves, piecePos, oppositeMoveRight):
        if not legalMoves:
            if not self.isCheck(piecePos, True, None, oppositeMoveRight):
                return True
        return False
    def testAllPositions(self, piecePos, moveRight, oppositeMoveRight, depth = 0, max_depth = 5, positions_seen = None):

        # Initialize the set of seen positions if not passed
        if positions_seen is None:
            positions_seen = set()

        if depth >= max_depth:
            # Convert the piecePos dictionary to a frozenset of tuples for hashing #hashthishashthathashitall
            position_key = frozenset(piecePos.items())
            positions_seen.add(position_key)
            return

        # Get all legal moves for the current player
        legalMoves = []
        legalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility)

        # Iterate through all legal moves
        for move in legalMoves:
            # Simulate the move
            newPiecePos = self.simulateMove(move, piecePos)

            # Recursively explore the next moves, change moveTight and oppositeMoveRight and increase the depth
            self.testAllPositions(newPiecePos, oppositeMoveRight, moveRight, depth + 1, max_depth, positions_seen)

        # Return the number of unique positions after x moves
        return len(positions_seen)

class Pawn(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self, moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility):
        rowW = "abcdefgh"
        columnW = "12345678"
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}P":
                blocked = False

                # Current position
                currentCol = rowW.index(position[0])
                currentRow = columnW.index(position[1])

                doubleForwardSquare = None
                # Calculate forward and diagonal squares
                if moveRight == "w":
                    if position[1] == "2":
                        doubleForwardSquare = f"{rowW[currentCol]}{columnW[currentRow + 2]}"
                    forwardSquare = f"{rowW[currentCol]}{columnW[currentRow + 1]}"
                    leftDiagonal = f"{rowW[currentCol - 1]}{columnW[currentRow + 1]}" if currentCol > 0 else None
                    rightDiagonal = f"{rowW[currentCol + 1]}{columnW[currentRow + 1]}" if currentCol < 7 else None
                else:  # Black pawn
                    if position[1] == "7":
                        doubleForwardSquare = f"{rowW[currentCol]}{columnW[currentRow - 2]}"
                    forwardSquare = f"{rowW[currentCol]}{columnW[currentRow - 1]}"
                    leftDiagonal = f"{rowW[currentCol - 1]}{columnW[currentRow - 1]}" if currentCol > 0 else None
                    rightDiagonal = f"{rowW[currentCol + 1]}{columnW[currentRow - 1]}" if currentCol < 7 else None
                move = f"{piece}{forwardSquare}"

                # Check forward movement
                if forwardSquare not in piecePos.values() and not self.isCheck(piecePos, False, move, oppositeMoveRight): # Not in check after move
                    if moveRight == "w" and columnW.index(forwardSquare[1]) == 7: #Promotion for white
                        legalMoves.append(f"{piece}{forwardSquare}Q")
                        legalMoves.append(f"{piece}{forwardSquare}N")
                        legalMoves.append(f"{piece}{forwardSquare}B")
                        legalMoves.append(f"{piece}{forwardSquare}R")
                    elif moveRight == "b" and columnW.index(forwardSquare[1]) == 0: #Promotion for black
                        legalMoves.append(f"{piece}{forwardSquare}Q")
                        legalMoves.append(f"{piece}{forwardSquare}N")
                        legalMoves.append(f"{piece}{forwardSquare}B")
                        legalMoves.append(f"{piece}{forwardSquare}R")
                    else:
                        legalMoves.append(f"{piece}{forwardSquare}")

                # Check diagonal captures
                for diagSquare in [leftDiagonal, rightDiagonal]:
                    if diagSquare and diagSquare in piecePos.values():
                        targetPiece = [p for p, pos in piecePos.items() if pos == diagSquare][0]
                        if targetPiece[0] != moveRight and not self.isCheck(piecePos, True, piece+diagSquare, oppositeMoveRight):  # Enemy piece and not in check after move
                            if moveRight == "w" and columnW.index(diagSquare[1]) == 7: #Promotion for white
                                legalMoves.append(f"{piece}{diagSquare}Q")
                                legalMoves.append(f"{piece}{diagSquare}N")
                                legalMoves.append(f"{piece}{diagSquare}B")
                                legalMoves.append(f"{piece}{diagSquare}R")
                            elif moveRight == "b" and columnW.index(diagSquare[1]) == 0: #Promotion for black
                                legalMoves.append(f"{piece}{diagSquare}Q")
                                legalMoves.append(f"{piece}{diagSquare}N")
                                legalMoves.append(f"{piece}{diagSquare}B")
                                legalMoves.append(f"{piece}{diagSquare}R")
                            else:
                                legalMoves.append(f"{piece}{diagSquare}")

                # Check double move
                if doubleForwardSquare:
                    if doubleForwardSquare not in piecePos.values() and forwardSquare not in piecePos.values() and not self.isCheck(piecePos, False, piece+doubleForwardSquare, oppositeMoveRight):
                        legalMoves.append(f"{piece}{doubleForwardSquare}")
                if moveRight == "w" and position[1] == "5" and enpassantPossibility[0] == "possible":
                    print("RECOGNIZED ENPASSANT POSSIBILITY")
                    lastMove = enpassantPossibility[1]
                    lastRow = rowW.index(lastMove[3])
                    if currentCol + 1 == lastRow:
                        legalMoves.append(f"{piece}{rightDiagonal}e.p")
                    if currentCol - 1 == lastRow:
                        legalMoves.append(f"{piece}{leftDiagonal}e.p")

                if moveRight == "b" and position[1] == "4" and enpassantPossibility[0] == "possible":
                    lastMove = enpassantPossibility[1]
                    lastRow = rowW.index(lastMove[3])
                    if currentCol + 1 == lastRow:
                        legalMoves.append(f"{piece}{rightDiagonal}e.p")
                    if currentCol - 1 == lastRow:
                        legalMoves.append(f"{piece}{leftDiagonal}e.p")

    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):
        rowW = "abcdefgh"
        columnW = "12345678"
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}P":
                blocked = False

                # Current position
                currentCol = rowW.index(position[0])
                currentRow = columnW.index(position[1])

                doubleForwardSquare = None
                # Calculate forward and diagonal squares
                if oppositeMoveRight == "w":
                    if position[1] == "2":
                        doubleForwardSquare = f"{rowW[currentCol]}{columnW[currentRow + 2]}"
                    forwardSquare = f"{rowW[currentCol]}{columnW[currentRow + 1]}"
                    leftDiagonal = f"{rowW[currentCol - 1]}{columnW[currentRow + 1]}" if currentCol > 0 else None
                    rightDiagonal = f"{rowW[currentCol + 1]}{columnW[currentRow + 1]}" if currentCol < 7 else None
                else:  # Black pawn
                    if position[1] == "7":
                        doubleForwardSquare = f"{rowW[currentCol]}{columnW[currentRow - 2]}"
                    forwardSquare = f"{rowW[currentCol]}{columnW[currentRow - 1]}"
                    leftDiagonal = f"{rowW[currentCol - 1]}{columnW[currentRow - 1]}" if currentCol > 0 else None
                    rightDiagonal = f"{rowW[currentCol + 1]}{columnW[currentRow - 1]}" if currentCol < 7 else None
                move = f"{piece}{forwardSquare}"

                # Check forward movement
                if forwardSquare not in piecePos.values():
                    if oppositeMoveRight == "w" and columnW.index(forwardSquare[1]) == 7: #Promotion for white
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}Q")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}N")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}B")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}R")
                    elif oppositeMoveRight == "b" and columnW.index(forwardSquare[1]) == 0: #Promotion for black
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}Q")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}N")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}B")
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}R")
                    else:
                        isCheckLegalMoves.append(f"{piece}{forwardSquare}")

                # Check diagonal captures
                for diagSquare in [leftDiagonal, rightDiagonal]:
                    if diagSquare and diagSquare in piecePos.values():
                        targetPiece = [p for p, pos in piecePos.items() if pos == diagSquare][0]
                        if targetPiece[0] != oppositeMoveRight:  # Enemy piece and not in check after move
                            if oppositeMoveRight == "w" and columnW.index(diagSquare[1]) == 7: #Promotion for white
                                isCheckLegalMoves.append(f"{piece}{diagSquare}Q")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}N")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}B")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}R")
                            elif oppositeMoveRight == "b" and columnW.index(diagSquare[1]) == 0: #Promotion for black
                                isCheckLegalMoves.append(f"{piece}{diagSquare}Q")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}N")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}B")
                                isCheckLegalMoves.append(f"{piece}{diagSquare}R")
                            else:
                                isCheckLegalMoves.append(f"{piece}{diagSquare}")

                # Check double move
                if doubleForwardSquare:
                    if doubleForwardSquare not in piecePos.values() and forwardSquare not in piecePos.values():
                        isCheckLegalMoves.append(f"{piece}{doubleForwardSquare}")
class Knight(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self ,moveRight, oppositeMoveRight, piecePos, legalMoves):
        column = "12345678"
        row = "abcdefgh"
        knightMoves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),  # L-shapes vertically
        (1, 2), (1, -2), (-1, 2), (-1, -2)   # L-shapes horizontally
    ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}N": # Find knights of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in knightMoves:
                    newCol = currentCol + colOffset
                    newRow = currentRow + rowOffset
                    if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                        destination = f"{row[newCol]}{column[newRow]}"
                        move = f"{piece}{destination}"

                        if destination in piecePos.values(): # When a piece is in the way
                            targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                            if targetPiece[0] != moveRight: # When its a opposite colored piece add it as legalMove
                                if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                    legalMoves.append(move)
                        else: # Else, if not in check add it as legalMove
                            if not self.isCheck(piecePos, True, move, oppositeMoveRight): 
                                legalMoves.append(move)

    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):
        column = "12345678"
        row = "abcdefgh"
        knightMoves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),  # L-shapes vertically
        (1, 2), (1, -2), (-1, 2), (-1, -2)   # L-shapes horizontally
    ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}N": # Find knights of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in knightMoves:
                    newCol = currentCol + colOffset
                    newRow = currentRow + rowOffset
                    if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                        destination = f"{row[newCol]}{column[newRow]}"
                        move = f"{piece}{destination}"

                        if destination in piecePos.values(): # When a piece is in the way
                            targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                            if targetPiece[0] != oppositeMoveRight: # When its a opposite colored piece add it as legalMove
                                isCheckLegalMoves.append(move)
                        else: # Else, if not in check add it as legalMove
                            isCheckLegalMoves.append(move)

class Bishop(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self ,moveRight, oppositeMoveRight, piecePos, legalMoves):

        column = "12345678"
        row = "abcdefgh"
        directions = [
                    (1, 1),   # Top-right
                    (1, -1),  # Bottom-right
                    (-1, 1),  # Top-left
                    (-1, -1)  # Bottom-left
                ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}B":
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for direction in directions:
                    colOffset, rowOffset = direction
                    step = 1
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8:
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"
                            if destination in piecePos.values():
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != moveRight:
                                    if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                        legalMoves.append(move)
                                break
                            else:
                                if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                    legalMoves.append(move)
                        else:
                            break
                        step += 1

    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):

        column = "12345678"
        row = "abcdefgh"
        directions = [
                    (1, 1),   # Top-right
                    (1, -1),  # Bottom-right
                    (-1, 1),  # Top-left
                    (-1, -1)  # Bottom-left
                ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}B":
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for direction in directions:
                    colOffset, rowOffset = direction
                    step = 1
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8:
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"
                            if destination in piecePos.values():
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != oppositeMoveRight:
                                    isCheckLegalMoves.append(move)
                                break
                            else:
                                isCheckLegalMoves.append(move)
                        else:
                            break
                        step += 1

class Rook(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self ,moveRight, oppositeMoveRight, piecePos, legalMoves):
        column = "12345678"
        row = "abcdefgh"

        rookMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}R": # Find rooks of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in rookMoves:
                    step = 1
                    
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"

                            if destination in piecePos.values(): # When a piece is in the way
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != moveRight: # When its a opposite colored piece add it as legalMove
                                    if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                        legalMoves.append(move)
                                break
                            else: # Else, if not in check add it as legalMove
                                if not self.isCheck(piecePos, True, move, oppositeMoveRight): 
                                    legalMoves.append(move)
                        else:
                            break
                        step += 1

    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):
        column = "12345678"
        row = "abcdefgh"

        rookMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}R": # Find rooks of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in rookMoves:
                    step = 1
                    
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"

                            if destination in piecePos.values(): # When a piece is in the way
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != oppositeMoveRight: # When its a opposite colored piece add it as legalMove
                                    isCheckLegalMoves.append(move)
                                break
                            else: # Else, if not in check add it as legalMove
                                isCheckLegalMoves.append(move)
                        else:
                            break
                        step += 1

class Queen(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self ,moveRight, oppositeMoveRight, piecePos, legalMoves):
        column = "12345678"
        row = "abcdefgh"

        queenMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
            (1, 1),   # Top-right
            (1, -1),  # Bottom-right
            (-1, 1),  # Top-left
            (-1, -1)  # Bottom-left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}Q": # Find queens of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in queenMoves:
                    step = 1
                    
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"

                            if destination in piecePos.values(): # When a piece is in the way
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != moveRight: # When its a opposite colored piece add it as legalMove
                                    if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                        legalMoves.append(move)
                                break
                            else: # Else, if not in check add it as legalMove
                                if not self.isCheck(piecePos, True, move, oppositeMoveRight): 
                                    legalMoves.append(move)
                        else:
                            break
                        step += 1

    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):
        column = "12345678"
        row = "abcdefgh"

        queenMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
            (1, 1),   # Top-right
            (1, -1),  # Bottom-right
            (-1, 1),  # Top-left
            (-1, -1)  # Bottom-left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}Q": # Find queens of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in queenMoves:
                    step = 1
                    
                    while True:
                        newCol = currentCol + step * colOffset
                        newRow = currentRow + step * rowOffset
                        if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                            destination = f"{row[newCol]}{column[newRow]}"
                            move = f"{piece}{destination}"

                            if destination in piecePos.values(): # When a piece is in the way
                                targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                                if targetPiece[0] != oppositeMoveRight: # When its a opposite colored piece add it as legalMove
                                    isCheckLegalMoves.append(move)
                                break
                            else: # Else, if not in check add it as legalMove
                                isCheckLegalMoves.append(move)
                        else:
                            break
                        step += 1

class King(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self ,moveRight, oppositeMoveRight, piecePos, legalMoves):
        column = "12345678"
        row = "abcdefgh"
        """
        Castling:
            The king and rook have not moved yet.
            The king is not in check.
            The king is not in check after castling.
            The king can move one square to the side (the side of the castling).
            The rook can move to a square next to the king.
            There is no piece on the square next to the king on the side of the castling.
        """
        kingMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
            (1, 1),   # Top-right
            (1, -1),  # Bottom-right
            (-1, 1),  # Top-left
            (-1, -1)  # Bottom-left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{moveRight}K": # Find King of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in kingMoves:
                    newCol = currentCol + colOffset
                    newRow = currentRow + rowOffset
                    if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                        destination = f"{row[newCol]}{column[newRow]}"
                        move = f"{piece}{destination}"

                        if destination in piecePos.values(): # When a piece is in the way
                            targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                            if targetPiece[0] != moveRight: # When its a opposite colored piece add it as legalMove
                                if not self.isCheck(piecePos, True, move, oppositeMoveRight):
                                    legalMoves.append(move)
                        else: # Else, if not in check add it as legalMove
                            if not self.isCheck(piecePos, True, move, oppositeMoveRight): 
                                legalMoves.append(move)
                if moveRight == "w":
                    if "wR1c1" in legalMoves and pieceMoveCount["wR1"] == 0 and pieceMoveCount["wK1"] == 0 and not self.isCheck(piecePos, True, None, oppositeMoveRight):
                        if not self.isCheck(piecePos, True, "wK1c1", oppositeMoveRight) and "c1" not in piecePos.values() and "wK1c1" in legalMoves:
                            legalMoves.append("w0-0-0")
                    elif "wR2f1" in legalMoves and pieceMoveCount["wR2"] == 0 and pieceMoveCount["wK1"] == 0 and not self.isCheck(piecePos, True, None, oppositeMoveRight):
                        if not self.isCheck(piecePos, True, "wK1g1", oppositeMoveRight) and "f1" not in piecePos.values() and "wK1f1" in legalMoves:
                            legalMoves.append("w0-0")

                elif moveRight == "b":
                    if "bR1c8" in legalMoves and pieceMoveCount["bR1"] == 0 and pieceMoveCount["bK1"] == 0 and not self.isCheck(piecePos, True, None, oppositeMoveRight):
                        if not self.isCheck(piecePos, True, "bK1c8", oppositeMoveRight) and "c8" not in piecePos.values() and "bK1c8" in legalMoves:
                            legalMoves.append("b0-0-0")
                    elif "bR2f8" in legalMoves and pieceMoveCount["bR2"] == 0 and pieceMoveCount["bK1"] == 0 and not self.isCheck(piecePos, True, None, oppositeMoveRight):
                        if not self.isCheck(piecePos, True, "bK1g8", oppositeMoveRight) and "f8" not in piecePos.values() and "bK1f8" in legalMoves:
                            legalMoves.append("b0-0")
        
    def isCheckGetLegalMoves(self,oppositeMoveRight,piecePos,isCheckLegalMoves):
        column = "12345678"
        row = "abcdefgh"
        """
        Castling:
            The king and rook have not moved yet.
            The king is not in check.
            The king is not in check after castling.
            The king can move one square to the side (the side of the castling).
            The rook can move to a square next to the king.
            There is no piece on the square next to the king on the side of the castling.
        """
        kingMoves =[
            (1,0),    # Up
            (-1,0),   # Down
            (0,1),    # Right
            (0,-1),   # Left
            (1, 1),   # Top-right
            (1, -1),  # Bottom-right
            (-1, 1),  # Top-left
            (-1, -1)  # Bottom-left
        ]
        for piece,position in piecePos.items():
            if piece[0:2] == f"{oppositeMoveRight}K": # Find King of the correct color
                currentCol = row.index(position[0])
                currentRow = column.index(position[1])

                for colOffset,rowOffset in kingMoves:
                    newCol = currentCol + colOffset
                    newRow = currentRow + rowOffset
                    if 0 <= newCol < 8 and 0 <= newRow < 8: # Ensure move is within bounds
                        destination = f"{row[newCol]}{column[newRow]}"
                        move = f"{piece}{destination}"

                        if destination in piecePos.values(): # When a piece is in the way
                            targetPiece = [p for p, pos in piecePos.items() if pos == destination][0]
                            if targetPiece[0] != oppositeMoveRight: # When its a opposite colored piece add it as legalMove
                                isCheckLegalMoves.append(move)
                        else: # Else, if not in check add it as legalMove
                            isCheckLegalMoves.append(move)

# Create class instances
piece = Piece()
bishop = Bishop()
knight = Knight()
rook = Rook()
queen = Queen()
king = King()

def getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves, enpassantPossibility):
    legalMoves = []
    pieceTypes = []
    for piece, position in piecePos.items():
        pieceColor = piece[0]  # 'w' or 'b'
        # Skip pieces that are not of the current player's color
        if pieceColor != moveRight:
            continue
        if piece[1] not in pieceTypes:
            pieceType = piece[1]
            pieceTypes.append(pieceType)
            
            if pieceType == "P":
                Pawn().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves,enpassantPossibility)
            elif pieceType == "B":
                Bishop().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
            elif pieceType == "R":
                Rook().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
            elif pieceType == "N":
                Knight().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
            elif pieceType == "B":
                Bishop().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
            elif pieceType == "Q":
                Queen().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
            elif pieceType == "K":
                King().getLegalMoves(moveRight, oppositeMoveRight, piecePos, legalMoves)
    return legalMoves

def getAllIsCheckLegalMoves(piecePos, moveRight, isCheckLegalMoves):
    isCheckLegalMoves = []
    isCheckPieceTypes = []
    for piece, position in piecePos.items():
        pieceColor = piece[0]  # 'w' or 'b'
        # Skip pieces that are not of the current player's color
        if pieceColor != moveRight:
            continue
        if piece[1] not in isCheckPieceTypes:
            pieceType = piece[1]
            isCheckPieceTypes.append(pieceType)
            
            if pieceType == "P":
                Pawn().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "B":
                Bishop().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "R":
                Rook().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "N":
                Knight().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "B":
                Bishop().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "Q":
                Queen().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
            elif pieceType == "K":
                King().isCheckGetLegalMoves(moveRight, piecePos, isCheckLegalMoves)
    return isCheckLegalMoves
class ChessBot:
    def chessBot(self, piecePos, moveRight, oppositeMoveRight, chessBotEnpassantPossibility, maxDepth, currentDepth=0, alpha = float("-inf"), beta = float("inf"),calculations = 0):

        chessBotLegalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, None, chessBotEnpassantPossibility)
        if currentDepth >= maxDepth:
            return None, self.evaluatePos(piecePos, chessBotLegalMoves, moveRight), calculations

        bestMove = None
        bestEvaluation = float('-inf') if moveRight == "w" else float('inf')  # Maximize for white, minimize for black

        for move in chessBotLegalMoves:
            isCapture = True
            if move[1] == "P":  # If the piece is a pawn:
                if move[3] == piecePos[move[0:3]][0]:  # Check if it's capturing
                    isCapture = False

            newPiecePos = piece.simulateMove(move, piecePos, isCapture)

            _, evaluation, calculations = self.chessBot(newPiecePos, oppositeMoveRight, moveRight, chessBotEnpassantPossibility, maxDepth, currentDepth + 1, alpha, beta, calculations)
            calculations += 1
            if moveRight == "w":  # Maximizing player:
                
                if evaluation > bestEvaluation:
                    bestEvaluation = evaluation
                    bestMove = move
                alpha = max(alpha, bestEvaluation)
                if beta <= alpha:
                    break
            else:  # Minimizing player
                
                if evaluation < bestEvaluation:
                    bestEvaluation = evaluation
                    bestMove = move
                beta = min(beta, bestEvaluation)
                if beta <= alpha:
                    break

        return bestMove, bestEvaluation, calculations

    def evaluatePos(self, piecePos, legalMoves, moveRight):
        eval = 0

        for move in legalMoves:
            if move == "w0-0" or move == "w0-0-0":
                eval += 1
            elif move == "b0-0" or move == "b0-0-0":
                eval -= 1
            elif moveRight == "w":
                eval += valueForLegalMoves[move[1]]
            elif moveRight == "b":
                eval -= valueForLegalMoves[move[1]]

        for piece in piecePos:
            if piece[0] == "w":
                if piece[1] == "P":
                    eval += pawn_square_values[piecePos[piece]]
                if piece[1] == "N":
                    eval += knight_square_values[piecePos[piece]]
                if piece[1] == "B":
                    eval += bishop_square_values[piecePos[piece]]
                if piece[1] == "R":
                    eval += rook_square_values[piecePos[piece]]
                if piece[1] == "Q":
                    eval += queen_square_values[piecePos[piece]]
                if piece[1] == "K":
                    eval += king_square_values[piecePos[piece]]
                eval += pieceValues[piece[1]]
            
            if piece[0] == "b":
                if piece[1] == "P":
                    eval -= pawn_square_values[piecePos[piece]]
                if piece[1] == "N":
                    eval -= knight_square_values[piecePos[piece]]
                if piece[1] == "B":
                    eval -= bishop_square_values[piecePos[piece]]
                if piece[1] == "R":
                    eval -= rook_square_values[piecePos[piece]]
                if piece[1] == "Q":
                    eval -= queen_square_values[piecePos[piece]]
                if piece[1] == "K":
                    eval -= king_square_values[piecePos[piece]]
                eval -= pieceValues[piece[1]]
            
        return eval
    
chessbot = ChessBot()