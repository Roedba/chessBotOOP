import pygame
"""
todo:
    implement the getLegalmoves function for the Pawn
    repeat for all pieces
"""
class Piece:
    def __init__(self):
        pass
    
    def move(self,move,pieceColor,piecePos,legalMoves):
        if move in legalMoves:
            piece = pieceColor + move[0:3]
            destination = move[4:6]
            #destination like a3 and piece like wR1
            piecePos[piece] = destination
            return True
            #if the piecePos dict is modified the passed dict is also modified(passing by reference)
        else:
            print(f"Illegal move: {piece} to {destination}")
            return False
            #if not a legal move return false

    def draw(self,piecePos,squareCoords,chessBoard,images):
        #specific function
        for piece in piecePos:
            extractedCoords = squareCoords[piecePos[piece]].split("|")
            pieceImage = images[piece]
            chessBoard.blit(pieceImage,(int(extractedCoords[0]),int(extractedCoords[1])))

    def getLegalMoves(self,moveRight,piecePos,board):
        #basic function structure, raise error if not implemented in subclass
        raise NotImplementedError("This method should be implemented by subclasses")

class Pawn(Piece):
    def __init__(self):
        super().__init__()

    def getLegalMoves(self,moveRight,piecePos,legalMoves):
        for piece in piecePos.items():
            if piece[0:2] == f"{moveRight}P":
                #wenn eine figur ein feld vor ihm steht oder wenn man nach dem zug im schach steht 
                #passiert nix
                #wenn eine figur diagonal steht kann der bauer auf das feld ziehen
                piecePosition = piecePos[piece]
                if moveRight == "w":
                    blocked = False
                    rowW = "abcdefgh"
                    columnW = "12345678"
                    frontSquare = f"{piecePosition[0]}{rowW.index(piecePosition[1]+1)}"
                    frontSideLeftSquare = f"{rowW[rowW.index(piecePosition[0]-1)]}{columnW[columnW.index(piecePosition[1]+1)]}"
                    frontSideRightSquare = f"{rowW[rowW.index(piecePosition[0]+1)]}{columnW[columnW.index(piecePosition[1]+1)]}"

                    for pieceSQ in piecePos.values():
                        if pieceSQ == frontSquare:
                            blocked = True
                        if pieceSQ == frontSideLeftSquare or pieceSQ == frontSideRightSquare and (piece[0:3] + pieceSQ) not in legalMoves:
                            legalMoves.append[piece[0:3] + pieceSQ]
                    if not blocked:
                        legalMoves.append[piece[0:3] + frontSquare]