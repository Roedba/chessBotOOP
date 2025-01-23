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
                    if doubleForwardSquare not in piecePos.values():
                        isCheckLegalMoves.append(f"{piece}{doubleForwardSquare}")