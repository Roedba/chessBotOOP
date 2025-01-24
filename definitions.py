import pygame

moveRight = "w"
oppositeMoveRight = "b"
moveInput = ""
legalMoves = []
isCheckLegalMoves =[]
clock = pygame.time.Clock()

rowW = "abcdefgh"
rowB = "hgfedcba"
columnW = "12345678"
columnB = "87654321"
move = None
enpassantPossibility = ["notPossible",None]

piecePosDict = {}
movesSinceLastCapture = [0]
pieceCount = {
    "wQ":1,"wK":1,"wB":2,"wN":2,"wP":8,"wR":2,"bQ":1,"bK":1,"bB":2,"bN":2,"bP":8,"bR":2
}
piece_pos = {
    "wR1": "a1", "wN1": "b1", "wB1": "c1", "wQ1": "d1", "wK1": "e1", "wB2": "f1", "wN2": "g1", "wR2": "h1",
    "bR1": "a8", "bN1": "b8", "bB1": "c8", "bQ1": "d8", "bK1": "e8", "bB2": "f8", "bN2": "g8", "bR2": "h8",
    "wP1": "a2", "wP2": "b2", "wP3": "c2", "wP4": "d2", "wP5": "e2", "wP6": "f2", "wP7": "g2", "wP8": "h2",
    "bP1": "a7", "bP2": "b7", "bP3": "c7", "bP4": "d7", "bP5": "e7", "bP6": "f7", "bP7": "g7", "bP8": "h7"
}
sq = {'a8': '42|25', 'b8': '101|25', 'c8': '160|25', 'd8': '219|25', 'e8': '278|25', 'f8': '337|25', 'g8': '396|25', 'h8': '455|25',
       'a7': '42|84', 'b7': '101|84', 'c7': '160|84', 'd7': '219|84', 'e7': '278|84', 'f7': '337|84', 'g7': '396|84', 'h7': '455|84',
         'a6': '42|143', 'b6': '101|143', 'c6': '160|143', 'd6': '219|143', 'e6': '278|143', 'f6': '337|143', 'g6': '396|143',
           'h6': '455|143', 'a5': '42|202', 'b5': '101|202', 'c5': '160|202', 'd5': '219|202', 'e5': '278|202', 'f5': '337|202',
             'g5': '396|202', 'h5': '455|202', 'a4': '42|261', 'b4': '101|261', 'c4': '160|261', 'd4': '219|261', 'e4': '278|261',
               'f4': '337|261', 'g4': '396|261', 'h4': '455|261', 'a3': '42|320', 'b3': '101|320', 'c3': '160|320', 'd3': '219|320',
                 'e3': '278|320', 'f3': '337|320', 'g3': '396|320', 'h3': '455|320', 'a2': '42|379', 'b2': '101|379', 'c2': '160|379',
                   'd2': '219|379', 'e2': '278|379', 'f2': '337|379', 'g2': '396|379', 'h2': '455|379', 'a1': '42|438', 'b1': '101|438',
                     'c1': '160|438', 'd1': '219|438', 'e1': '278|438', 'f1': '337|438', 'g1': '396|438', 'h1': '455|438'}

pieceMoveCount = {
    "wR1": 0, "wN1": 0, "wB1": 0, "wQ1": 0, "wK1": 0, "wB2": 0, "wN2": 0, "wR2": 0,
    "bR1": 0, "bN1": 0, "bB1": 0, "bQ1": 0, "bK1": 0, "bB2": 0, "bN2": 0, "bR2": 0,
    "wP1": 0, "wP2": 0, "wP3": 0, "wP4": 0, "wP5": 0, "wP6": 0, "wP7": 0, "wP8": 0,
    "bP1": 0, "bP2": 0, "bP3": 0, "bP4": 0, "bP5": 0, "bP6": 0, "bP7": 0, "bP8": 0
}
# List of drawn piece configurations
drawnConfigurations = [
    # King vs. King
    {"wK1": "e1", "bK1": "e8"},

    # King and Bishop vs. King
    {"wK1": "e1", "wB1": "c3", "bK1": "e8"},

    # King and Knight vs. King
    {"wK1": "e1", "wN1": "f3", "bK1": "e8"},

    # King and Bishop vs. King and Bishop (same color)
    {"wK1": "e1", "wB1": "c3", "bK1": "e8", "bB1": "f6"},

    # King and Knight vs. King and Knight
    {"wK1": "e1", "wN1": "f3", "bK1": "e8", "bN1": "g6"},

    # King and Bishop vs. King and Knight
    {"wK1": "e1", "wB1": "c3", "bK1": "e8", "bN1": "g6"},

    # King vs. King and Bishop
    {"wK1": "e1", "bK1": "e8", "bB1": "f6"},

    # King vs. King and Knight
    {"wK1": "e1", "bK1": "e8", "bN1": "g6"},

    # King and Bishop vs. King and Bishop (opposite color)
    {"wK1": "e1", "wB1": "c3", "bK1": "e8", "bB1": "c6"},
]
def load_pieces():
    # List of piece types
    piece_types = ["R", "N", "B", "Q", "K", "P"]  # Rook, Knight, Bishop, Queen, King, Pawn
    
    # Number of each piece type
    piece_counts = {
        "R": 8,  # Two rooks
        "N": 8,  # Two knights
        "B": 8,  # Two bishops
        "Q": 8,  # One queen
        "K": 1,  # One king
        "P": 8   # Eight pawns
    }

    # Colors for pieces
    colors = ["w", "b"]  # White and Black
    
    # Dictionary to store preloaded images
    images = {}

    # Load all piece images
    for color in colors:
        for piece_type, count in piece_counts.items():
            for i in range(1, count + 1):  # Iterate over piece numbers
                piece_name = f"{color}{piece_type}{i}"  # Example: wR1, bP8
                image_path = f"images/{piece_name}.png"  # Path to the image file
                try:
                    images[piece_name] = pygame.image.load(image_path)  # Load the image
                except FileNotFoundError:
                    print(f"Image not found: {image_path}")  # Handle missing images gracefully

    return images
images = load_pieces()