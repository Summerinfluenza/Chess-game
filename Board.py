from collections import OrderedDict, Counter
from Pieces import BlackPawn, WhitePawn, Rook, Knight, Bishop, Queen, King

WHITE = "RNBQKBNRP"
BLACK = "rnbqkbnrp"
CHARS = "abcdefgh"
EMPTY = "- "


class Board:
    def __init__(self):
        # Chess boards
        self.clear_board = OrderedDict()
        self.play_board = OrderedDict()
        self.player_turn = "white"
        self.status = ""
        self.turn_count = 2
        self.previous_piece = ""

        # Occupied slots
        self.all_occupied = []
        self.white_occupied = []
        self.black_occupied = []

        # Player king positions
        self.white_king = (5, 1)
        self.black_king = (5, 8)

        # Player moves
        self.white_moves = []
        self.black_moves = []

        # Player captured
        self.white_captured = []
        self.black_captured = []

    # ----------Board methods----------
    # Creates a clear board
    def create_board(self):
        for index in range(8, 0, -1):
            for num in range(1, 9):
                self.clear_board[str(num) + str(index)] = EMPTY

    # Fill a clear board with pieces at their default positions
    def default_board(self):
        # Need to first create a clear board
        self.create_board()

        # Creating the pawns and fill them into their default positions
        for num in range(1, 9):
            self.clear_board[str(num) + str(7)] = self.create_piece(name="p", pos=(num, 7))

        for num in range(1, 9):
            self.clear_board[str(num) + str(2)] = self.create_piece(name="P", pos=(num, 2))

        # Creating other pieces and fill them into their default positions
        # Black pieces
        for num, piece in zip(range(1, 9), BLACK):
            self.clear_board[str(num) + str(8)] = self.create_piece(name=piece, pos=(num, 8))

        # White pieces
        for num, piece in zip(range(1, 9), WHITE):
            self.clear_board[str(num) + str(1)] = self.create_piece(name=piece, pos=(num, 1))

        self.play_board = self.clear_board

    # Creating three lists of occupied squares: white, black and all
    def occupied_slots(self):
        self.all_occupied = []
        self.black_occupied = []
        self.white_occupied = []

        for square in self.play_board.values():
            if square != EMPTY:
                if square.name.islower():
                    self.black_occupied.append(square.pos)
                elif square.name.isupper():
                    self.white_occupied.append(square.pos)
        self.all_occupied = self.black_occupied + self.white_occupied

    # Returning the item name in (x, y)
    def check_position(self, pos):
        index = str(pos[0]) + str(pos[1])
        if not isinstance(self.play_board[index], str):
            return self.play_board[index].name
        else:
            return "- "

    # Printing a 2D chess board
    def print_board(self):
        # Top section
        print(self.player_turn.capitalize().center(30))
        print(f"Turn: {str(int(self.turn_count / 2))}".center(30))
        print(f"Status: {self.status}".center(30))
        print("    ", end="")
        for char in CHARS:
            print(char + " ", end=" ")

        # Top divider
        print("")
        print("   " + "_" * 26)
        print("8  |", end="")

        # Middle section
        count = 0
        index = 7
        for value in self.play_board.values():
            if count == 8:
                count = 1
                if isinstance(value, str):
                    print(f"|\n{index}  |{value}", end=" ")
                    index -= 1
                else:
                    print(f"|\n{index}  |{value.name} ", end=" ")
                    index -= 1
            else:
                if isinstance(value, str):
                    print(f"{value}", end=" ")
                else:
                    print(f"{value.name} ", end=" ")
                count += 1

        # Bottom divider
        print("|")
        print("   " + "_" * 26)

        # Bottom section
        print(f"White captured: {list(Counter(self.white_captured))}")
        print(f"White moves: {self.white_moves}")
        print("-" * 30)
        print(f"Black captured: {list(Counter(self.black_captured))}")
        print(f"Black moves: {self.black_moves}")
        print("-" * 30)

    # Creating chess pieces
    def create_piece(self, name, pos):
        if name == "p":
            pawn = BlackPawn()
            pawn.name = name
            pawn.pos = pos
            return pawn

        elif name == "P":
            pawn = WhitePawn()
            pawn.name = name
            pawn.pos = pos
            return pawn

        elif name == "r" or name == "R":
            rook = Rook()
            rook.name = name
            rook.pos = pos
            return rook

        elif name == "n" or name == "N":
            knight = Knight()
            knight.name = name
            knight.pos = pos
            return knight

        elif name == "b" or name == "B":
            bishop = Bishop()
            bishop.name = name
            bishop.pos = pos
            return bishop

        elif name == "q" or name == "Q":
            queen = Queen()
            queen.name = name
            queen.pos = pos
            return queen

        elif name == "k" or name == "K":
            king = King()
            king.name = name
            king.pos = pos
            return king

    # ----------Gameplay methods----------
    # Player move
    def player_move(self):
        # Asking for move inputs
        piece = input("Piece to move: ")

        # Checking if castling move
        if piece.lower() == "c":
            return self.castling(move=piece)

        raw_from_pos = input("From position: ")
        raw_to_pos = input("To position: ")

        # Checking for the correct inputs
        try:
            from_pos = (CHARS.index(raw_from_pos[0]) + 1, int(raw_from_pos[1]))
            to_pos = (CHARS.index(raw_to_pos[0]) + 1, int(raw_to_pos[1]))

        except (KeyError, ValueError, TypeError, IndexError):
            return False

        # Converting from pos(x, y) format into string "pos" format to access the dictionary
        from_index = str(from_pos[0]) + str(from_pos[1])
        to_index = str(to_pos[0]) + str(to_pos[1])

        # Checking if all the conditions are met according to the rules
        if self.valid_move(piece=piece, to_pos=to_pos, from_index=from_index):

            # Checking if the move will generate a self check
            if self.ghost_moving(from_pos=from_pos, to_pos=to_pos):

                # Captured piece to their respective lists
                self.capture_piece(to_index=to_index)

                # Moving the chess piece to the new position
                self.moving_piece(from_pos=from_pos, to_pos=to_pos)
                self.move_logs(from_data=raw_from_pos, to_data=raw_to_pos)

                return True

            else:
                return False
        else:
            return False

    # Checking if it's a valid move from the move_pattern
    def valid_move(self, piece, to_pos, from_index):

        # Payers can only move their own pieces
        if self.player_turn == "white":
            piece = piece.upper()
        elif self.player_turn == "black":
            piece = piece.lower()

        # Checking if the name input is correct
        if self.play_board[from_index] != EMPTY:
            if self.play_board[from_index].name == piece:

                # Generating a valid move pattern according to the rules, stops at blockade,
                # removing the last block if it's a friendly collision
                self.occupied_slots()

                if self.player_turn == "white":
                    self.play_board[from_index].move_patterns(friendly_occupied=self.white_occupied,
                                                              all_occupied=self.all_occupied)
                elif self.player_turn == "black":
                    self.play_board[from_index].move_patterns(friendly_occupied=self.black_occupied,
                                                              all_occupied=self.all_occupied)

                # Returning True if player move is in the piece eligible move pattern
                if to_pos in self.play_board[from_index].move_pattern:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # Capture piece
    def capture_piece(self, to_index):
        if self.play_board[to_index] != EMPTY:
            # capturing pieces of opposite colors
            if self.play_board[to_index].name in WHITE:
                self.black_captured.append(self.play_board[to_index].name)
            elif self.play_board[to_index].name in BLACK:
                self.white_captured.append(self.play_board[to_index].name)

    # Just moving a piece
    def moving_piece(self, from_pos, to_pos):
        from_index = str(from_pos[0]) + str(from_pos[1])
        to_index = str(to_pos[0]) + str(to_pos[1])

        # Assigning new attributes to the piece: pos, condition
        self.play_board[to_index] = self.play_board[from_index]
        self.play_board[to_index].condition = "changed"
        self.play_board[to_index].pos = to_pos

        # Filling the from_pos with an empty indicator
        self.play_board[from_index] = EMPTY

        # If the king moves, save its pos to the board also
        self.king_pos(pos=to_pos)

        # Checks if the pawns can be promoted
        self.pawn_upgrade(pos=to_pos)

    def ghost_moving(self, from_pos, to_pos):
        from_index = str(from_pos[0]) + str(from_pos[1])
        to_index = str(to_pos[0]) + str(to_pos[1])

        # Temporary storing the from_value
        from_index_piece = self.play_board[from_index]
        to_index_piece = self.play_board[to_index]

        # Assigning new attributes to the piece: pos
        self.play_board[to_index] = self.play_board[from_index]
        self.play_board[to_index].pos = to_pos

        # Filling the from_pos with an empty indicator
        self.play_board[from_index] = EMPTY

        # If the king moves, save its pos to the board also
        self.king_pos(pos=to_pos)

        if self.check():

            # Reverting all changes
            self.play_board[from_index] = from_index_piece
            self.play_board[from_index].pos = from_pos

            self.play_board[to_index] = to_index_piece
            if not isinstance(self.play_board[to_index], str):
                self.play_board[to_index].pos = to_pos
            self.king_pos(pos=from_pos)
            return False
        else:
            self.play_board[from_index] = from_index_piece
            self.play_board[from_index].pos = from_pos

            self.play_board[to_index] = to_index_piece
            if not isinstance(self.play_board[to_index], str):
                self.play_board[to_index].pos = to_pos
            self.king_pos(pos=from_pos)
            return True

    # Always save the king positions for check and castling methods
    def king_pos(self, pos):
        index = str(pos[0]) + str(pos[1])
        if self.play_board[index].name == "k":
            self.black_king = pos

        elif self.play_board[index].name == "K":
            self.white_king = pos

    # Move logs
    def move_logs(self, from_data, to_data):
        if self.player_turn == "white":
            self.white_moves.append([from_data + " ➡ " + to_data])
        elif self.player_turn == "black":
            self.black_moves.append([from_data + " ➡ " + to_data])

    # Special move - Castling
    def castling(self, move):

        # top right
        if move == "c" and self.player_turn == "black":
            if self.play_board["58"].condition == "unchanged" and self.play_board["88"].condition == "unchanged":
                for num in range(6, 8):
                    if self.check_position(pos=(num, 8)) != "- ":
                        print("Invalid move")
                        return False

                # moving the king and rook if all the conditions are met
                self.moving_piece("58", "78")
                self.moving_piece("88", "68")
                self.black_king = (7, 8)
                self.black_moves.append(["o-o"])
                return True

        # top left
        if move == "C" and self.player_turn == "black":
            if self.play_board["58"].condition == "unchanged" and self.play_board["18"].condition == "unchanged":
                for num in range(2, 5):
                    if self.check_position(pos=(num, 8)) != "- ":
                        print("Invalid move")
                        return False

                # moving the king and rook if all the conditions are met
                self.moving_piece("58", "28")
                self.moving_piece("18", "38")
                self.black_king = (2, 8)
                self.black_moves.append(["o-o-o"])
                return True

        # bottom left
        if move == "C" and self.player_turn == "white":
            if self.play_board["51"].condition == "unchanged" and self.play_board["11"].condition == "unchanged":
                for num in range(2, 5):
                    if self.check_position(pos=(num, 1)) != "- ":
                        print("Invalid move")
                        return False

                        # moving the king and rook if all the conditions are met
                    self.moving_piece("51", "21")
                    self.moving_piece("11", "31")
                    self.white_king = (2, 1)
                    self.white_moves.append(["o-o-o"])
                    return True

        # bottom right
        elif move == "c" and self.player_turn == "white":
            if self.play_board["51"].condition == "unchanged" and self.play_board["81"].condition == "unchanged":
                for num in range(6, 8):
                    if self.check_position(pos=(num, 1)) != "- ":
                        print("Invalid move")
                        return False

                        # moving the king and rook if all the conditions are met
                    self.moving_piece("51", "71")
                    self.moving_piece("81", "61")
                    self.white_king = (7, 1)
                    self.white_moves.append(["o-o"])
                    return True

    # Special move - Pawn upgrade
    def pawn_upgrade(self, pos):
        index = str(pos[0]) + str(pos[1])

        if self.play_board[index].name.lower() == "p":

            # If any pawn reaches the top or bottom of the board
            if pos[1] == 8 or pos[1] == 1:
                # Players having the option to choose an upgrade piece
                upgrade = input("Choose upgrade, q, r, n or b: ")
                try:
                    if self.play_board[index].name == "p":
                        self.play_board[index] = self.create_piece(name=upgrade.lower(), pos=pos)

                    elif self.play_board[index].name == "P":
                        self.play_board[index] = self.create_piece(name=upgrade.upper(), pos=pos)

                except (KeyError, ValueError, TypeError, IndexError):
                    print("Wrong upgrade")

    # Check
    def check(self):
        self.occupied_slots()
        moves = set()

        # Checking if the king can be checked by opponent's pieces, aka if the king is in their move patterns
        if self.player_turn == "white":
            for pos in self.black_occupied:
                self.play_board[str(pos[0]) + str(pos[1])].move_patterns(friendly_occupied=self.black_occupied,
                                                                         all_occupied=self.all_occupied)
                moves.update(self.play_board[str(pos[0]) + str(pos[1])].move_pattern)
            moves = list(moves)
            if self.white_king in moves:
                return True

        elif self.player_turn == "black":
            for pos in self.white_occupied:
                self.play_board[str(pos[0]) + str(pos[1])].move_patterns(friendly_occupied=self.white_occupied,
                                                                         all_occupied=self.all_occupied)
                moves.update(self.play_board[str(pos[0]) + str(pos[1])].move_pattern)
            moves = list(moves)
            if self.black_king in moves:
                return True

    # Checkmate
    def check_mate(self):
        self.occupied_slots()
        occupied = []

        if self.player_turn == "white":
            occupied = self.white_occupied
        elif self.player_turn == "black":
            occupied = self.black_occupied

        # Simulating all the possible moves, returning True if there's a possible move that nulls the check status
        for from_pos in occupied:
            from_index = str(from_pos[0]) + str(from_pos[1])
            for to_pos in self.play_board[from_index].move_patterns(friendly_occupied=occupied,
                                                                    all_occupied=self.all_occupied):
                if to_pos not in occupied:
                    # Checking if the simulated move is valid
                    if self.ghost_moving(from_pos=from_pos, to_pos=to_pos):
                        return False
        return True

    # Draw
    def draw(self):
        pass