import pygame
"""
todo:
    implement the getLegalmoves function for all pieces

    Objectives:
        implement check
        implement checkmate and stalemate
    Special Moves:
        implement promotion
        implement en passant
        implement castling, long and short(as king move?)

    Draw rules:
        3 move repetition
        50 move rule
        insufficient material to checkmate

    Extras:
        option to take back moves
"""
class Piece:
    def __init__(self):
        pass
    
    def move(self,move,pieceColor,piecePos,legalMoves):
        if move in legalMoves:
            piece = move[0:3]
            destination = move[3:5]
            # Destination like a3 and piece like wR1
            piecePos[piece] = destination # If the piecePos dict is modified the passed dict is also modified(passing by reference)
            for loopPiece,position in piecePos.items(): # delete piece if taken
                if position == destination and loopPiece != piece:
                    del piecePos[loopPiece]
                    return True
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
    
    def isCheck(self,piecePos,move):
        # Check if King is in Check after a move
        return False

class Pawn(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
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
                if forwardSquare not in piecePos.values() and not self.isCheck(piecePos,move): # Not in check after move
                    legalMoves.append(f"{piece}{forwardSquare}")

                # Check diagonal captures
                for diagSquare in [leftDiagonal, rightDiagonal]:
                    if diagSquare and diagSquare in piecePos.values():
                        targetPiece = [p for p, pos in piecePos.items() if pos == diagSquare][0]
                        if targetPiece[0] != moveRight and not self.isCheck(piecePos,move):  # Enemy piece and not in check after move
                            legalMoves.append(f"{piece}{diagSquare}")
                
                # Check double move
                if doubleForwardSquare:
                    if doubleForwardSquare not in piecePos.values() and not self.isCheck(piecePos,move):
                        legalMoves.append(f"{piece}{doubleForwardSquare}")

class Knight(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
        pass

class Bishop(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):

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
                                    if not self.isCheck(piecePos, move):
                                        legalMoves.append(move)
                                break
                            else:
                                if not self.isCheck(piecePos, move):
                                    legalMoves.append(move)
                        else:
                            break
                        step += 1

class Rook(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
        pass

class Queen(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
        pass

class King(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
        pass

def getAllLegalMoves(piecePos, moveRight, legalMoves):
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
                Pawn().getLegalMoves(moveRight, piecePos, legalMoves)
            """
            elif pieceType == "R":
                Rook().getLegalMoves(moveRight, piecePos, board, legalMoves)
            elif pieceType == "N":
                Knight().getLegalMoves(moveRight, piecePos, board, legalMoves)
            elif pieceType == "B":
                Bishop().getLegalMoves(moveRight, piecePos, board, legalMoves)
            elif pieceType == "Q":
                Queen().getLegalMoves(moveRight, piecePos, board, legalMoves)
            elif pieceType == "K":
                King().getLegalMoves(moveRight, piecePos, board, legalMoves)"""
    return legalMoves
