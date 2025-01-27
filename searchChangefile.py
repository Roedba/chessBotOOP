def chessBot(piecePos, moveRight, oppositeMoveRight, chessBotEnpassantPossibility, maxDepth, currentDepth = 0):

	chessBotLegalMoves = getAllLegalMoves(moveRight, oppositeMoveRight, piecePos, None, chessBotEnpassantPossibility)
	if currentDepth >= maxDepth:
		return None, eval(piecePos, chessBotLegalMoves)
	
	bestMove = None
	bestEvaluation = float('-inf') if moveRight == "w" else float('inf')  # Maximize for white, minimize for black

    for move in chessBotLegalMoves:
		isCapture = True
        if move[1] == "P":  # If the piece is a pawn:
            if move[3] == piecePos[move[0:3]][1]:  # Check if it's capturing
                isCapture = False
		
        newPiecePos = piece.simulateMove(move, piecePos, isCapture)

        _, evaluation = chessBot(newPiecePos, oppositeMoveRight, moveRight, chessBotEnpassantPossibility, maxDepth, currentDepth + 1)

	if moveRight == "w":  # Maximizing player:
        if evaluation > bestEvaluation:
            bestEvaluation = evaluation
            bestMove = move
    else:  # Minimizing player
        if evaluation < bestEvaluation:
        bestEvaluation = evaluation
        bestMove = move

	return bestMove, bestEvaluation
