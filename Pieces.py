class Pieces:
    def __init__(self):
        # Piece attributes
        self.condition = "unchanged"
        self.pos = (0, 0)
        self.name = ""
        self.move_pattern = []
        self.occupied = []

    # Generating a valid pattern by limiting it to a 8x8 board,
    # Removing all pos that are friendly occupied

    def valid_pattern(self, pattern, friendly_occupied):
        pattern = [pos for pos in pattern if 1 <= pos[0] < 9]
        pattern = [pos for pos in pattern if 1 <= pos[1] < 9]
        pattern = [pos for pos in pattern if pos not in friendly_occupied]
        self.move_pattern = pattern


class BlackPawn(Pieces):

    def __init__(self):
        super().__init__()

        self.name = "p"

    def move_patterns(self, friendly_occupied, all_occupied=None):
        self.move_pattern = []

        # All black pawn moves
        if (self.pos[0], self.pos[1] - 1) not in all_occupied:
            self.move_pattern.append((self.pos[0], self.pos[1] - 1))

        if self.condition == "unchanged" and (self.pos[0], self.pos[1] - 2) not in all_occupied:
            self.move_pattern.append((self.pos[0], self.pos[1] - 2))

        if (self.pos[0] - 1, self.pos[1] - 1) in all_occupied:
            if (self.pos[0] - 1, self.pos[1] - 1) not in friendly_occupied:
                self.move_pattern.append((self.pos[0] - 1, self.pos[1] - 1))

        if (self.pos[0] + 1, self.pos[1] - 1) in all_occupied:
            if (self.pos[0] + 1, self.pos[1] - 1) not in friendly_occupied:
                self.move_pattern.append((self.pos[0] + 1, self.pos[1] - 1))

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern


class WhitePawn(Pieces):

    def __init__(self):
        super().__init__()

        self.name = "P"

    def move_patterns(self, friendly_occupied, all_occupied=None):
        self.move_pattern = []

        # All black pawn moves
        if (self.pos[0], self.pos[1] + 1) not in all_occupied:
            self.move_pattern.append((self.pos[0], self.pos[1] + 1))

        if self.condition == "unchanged" and (self.pos[0], self.pos[1] + 2) not in all_occupied:
            self.move_pattern.append((self.pos[0], self.pos[1] + 2))

        if (self.pos[0] - 1, self.pos[1] + 1) in all_occupied:
            if (self.pos[0] - 1, self.pos[1] + 1) not in friendly_occupied:
                self.move_pattern.append((self.pos[0] - 1, self.pos[1] + 1))

        if (self.pos[0] + 1, self.pos[1] + 1) in all_occupied:
            if (self.pos[0] + 1, self.pos[1] + 1) not in friendly_occupied:
                self.move_pattern.append((self.pos[0] + 1, self.pos[1] + 1))

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern


class Rook(Pieces):

    def __init__(self):
        super().__init__()

    def move_patterns(self, friendly_occupied, all_occupied=None):
        self.move_pattern = []

        # Generating all the possible positions starting from self.pos
        # Horizontal to right moves ➡
        for num in range(self.pos[0] + 1, 9):
            self.move_pattern.append((num, self.pos[1]))
            if (num, self.pos[1]) in all_occupied:
                break

        # Horizontal to left moves ⬅
        for num in range(self.pos[0] - 1, - 1, -1):
            self.move_pattern.append((num, self.pos[1]))
            if (num, self.pos[1]) in all_occupied:
                break

        # Vertical up moves ⬆
        for num in range(self.pos[1] + 1, 9):
            self.move_pattern.append((self.pos[0], num))
            if (self.pos[0], num) in all_occupied:
                break

        # Vertical down moves ⬇
        for num in range(self.pos[1] - 1, - 1, -1):
            self.move_pattern.append((self.pos[0], num))
            if (self.pos[0], num) in all_occupied:
                break

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)

        return self.move_pattern


class Knight(Pieces):

    def __init__(self):
        super().__init__()

    def move_patterns(self, friendly_occupied, all_occupied=None):
        # All knight moves
        self.move_pattern = [(self.pos[0] - 1, self.pos[1] - 2), (self.pos[0] - 2, self.pos[1] - 1),
                             (self.pos[0] + 1, self.pos[1] - 2), (self.pos[0] + 2, self.pos[1] - 1),
                             (self.pos[0] - 1, self.pos[1] + 2), (self.pos[0] - 2, self.pos[1] + 1),
                             (self.pos[0] + 1, self.pos[1] + 2), (self.pos[0] + 2, self.pos[1] + 1)]

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern


class Bishop(Pieces):

    def __init__(self):
        super().__init__()

    def move_patterns(self, friendly_occupied, all_occupied=None):
        self.move_pattern = []

        # Generating all the possible positions starting from self.pos
        # 45 ↗
        for xpos, ypos in zip(range(self.pos[0] + 1, 9), range(self.pos[1] + 1, 9)):
            self.move_pattern.append((xpos, ypos))
            if (xpos, ypos) in all_occupied:
                break

        # 135 ↖
        for xpos, ypos in zip(range(self.pos[0] - 1, 0, -1), range(self.pos[1] + 1, 9)):
            self.move_pattern.append((xpos, ypos))
            if (xpos, ypos) in all_occupied:
                break

        # 225 ↙
        for xpos, ypos in zip(range(self.pos[0] - 1, 0, -1), range(self.pos[1] - 1, 0, -1)):
            self.move_pattern.append((xpos, ypos))
            if (xpos, ypos) in all_occupied:
                break

        # 315 ↘
        for xpos, ypos in zip(range(self.pos[0] + 1, 9), range(self.pos[1] - 1, 0, -1)):
            self.move_pattern.append((xpos, ypos))
            if (xpos, ypos) in all_occupied:
                break

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern


class Queen(Bishop, Rook):

    def __init__(self):
        Bishop.__init__(self)
        Rook.__init__(self)

    def move_patterns(self, friendly_occupied, all_occupied=None):

        # Queen is a combination of rook and bishop
        Rook.move_patterns(self, friendly_occupied, all_occupied)
        temp_storage = self.move_pattern
        Bishop.move_patterns(self, friendly_occupied, all_occupied)
        self.move_pattern += temp_storage

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern


class King(Pieces):

    def __init__(self):
        super(King, self).__init__()

    def move_patterns(self, friendly_occupied, all_occupied=None):
        # All king moves
        self.move_pattern = []
        for xpos in range(self.pos[0] - 1, self.pos[0] + 2):
            for ypos in range(self.pos[1] - 1, self.pos[1] + 2):
                self.move_pattern.append((xpos, ypos))

        self.valid_pattern(pattern=self.move_pattern, friendly_occupied=friendly_occupied)
        return self.move_pattern



