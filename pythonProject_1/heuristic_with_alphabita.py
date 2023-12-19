"""
Basic 3D Tic Tac Toe with Minimax and Alpha-Beta pruning, using a simple
heuristic to check for possible winning moves or blocking moves if no better
alternative exists.
"""
class Board(object):
    """3D TTT logic and underlying game state object.

    Attributes:
        board (List[List[List[int]]]): 3D array of positions.
        allowed_moves (List[int]): List of currently unoccupied positions.
        difficulty (int): Ply; number of moves to look ahead.
        depth_count (int): Used in conjunction with ply to control depth.
        human_turn (bool): Control whose turn it is.
        human (str): The Human's character.
        ai (str): The AI's character.
        players (tuple): Tuple of the Human and AI's characters.

    Args:
        human_first (Optional[bool]): Whether or no the computer goes second.
        human (Optional[str]): Human's character.
        ai (Optional[str]): AI's character.
        ply (Optional[int]): Number of moves to look ahead.
    """

    winning_combos = (
        # Rows on single board
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
        [16, 17, 18, 19], [20, 21, 22, 23], [24, 25, 26, 27], [28, 29, 30, 31],
        [32, 33, 34, 35], [36, 37, 38, 39], [40, 41, 42, 43], [44, 45, 46, 47],
        [48, 49, 50, 51], [52, 53, 54, 55], [56, 57, 58, 59], [60, 61, 62, 63],

        # Columns on single board
        [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
        [16, 20, 24, 28], [17, 21, 25, 29], [18, 22, 26, 30], [19, 23, 27, 31],
        [32, 36, 40, 44], [33, 37, 41, 45], [34, 38, 42, 46], [35, 39, 43, 47],
        [48, 52, 56, 60], [49, 53, 57, 61], [50, 54, 58, 62], [51, 55, 59, 63],

        # Diagonals on single board
        [0, 5, 10, 15], [3, 6, 9, 12],
        [16, 21, 26, 31], [19, 22, 25, 28],
        [32, 37, 42, 47], [35, 38, 41, 44],
        [48, 53, 58, 63], [51, 54, 57, 60],

        # Straight down through boards
        [0, 16, 32, 48], [1, 17, 33, 49], [2, 18, 34, 50], [3, 19, 35, 51],
        [4, 20, 36, 52], [5, 21, 37, 53], [6, 22, 38, 54], [7, 23, 39, 55],
        [8, 24, 40, 56], [9, 25, 41, 57], [10, 26, 42, 58], [11, 27, 43, 59],
        [12, 28, 44, 60], [13, 29, 45, 61], [14, 30, 46, 62], [15, 31, 47, 63],

        # Diagonals through boards
        [0, 20, 40, 60], [1, 21, 41, 61], [2, 22, 42, 62], [3, 23, 43, 63],
        [12, 24, 36, 48], [13, 25, 37, 49], [14, 26, 38, 50], [15, 27, 39, 51],
        [4, 21, 38, 55], [8, 25, 42, 59], [7, 22, 37, 52], [11, 26, 41, 56],
        [0, 17, 34, 51], [3, 18, 33, 48], [12, 29, 46, 63], [15, 30, 45, 60],
        [0, 21, 42, 63], [3, 22, 41, 60], [12, 25, 38, 51], [15, 26, 37, 48],
    )

    def __init__(self, human_first=True, human='X', ai='O', ply=1):
        self.board = Board.create_board()
        self.allowed_moves = list(range(pow(4, 3)))
        self.difficulty = ply
        self.depth_count = 0
        self.human_turn = human_first
        self.human = human
        self.ai = ai
        self.players = (human, ai)

    def reset(self):
        """Reset the game state."""
        self.allowed_moves = list(range(pow(4, 3)))
        self.board = Board.create_board()
        self.depth_count = 0

    def find(self, arr, key):
        """Find a given key in a 3D array.

        Args:
            arr (List[List[List[int]]]]): 3D array to search.
            key (int): Key to find.

        Returns:
            Tuple of the Board, Row, and Column of the key.
        """
        cnt = 0
        for i in range(4):
            for x in range(4):
                for y in range(4):
                    if cnt == key:
                        return i, x, y
                    cnt += 1

    def find_combo(self, combo):
        """Given a combination find the coordinates of each part.

        Args:
            combo (List[int]): Winning combination to search for.

        Returns:
            List of the coordinates of the starting, middle, and ending.
        """
        s, m, e = combo
        s = self.find(self.board, s)
        m = self.find(self.board, m)
        e = self.find(self.board, e)
        return s, m, e

    @staticmethod
    def create_board():
        """Create the board with appropriate positions and the like

        Returns:
            3D array with ints for each position.
        """
        cnt = 0
        board = []
        for i in range(4):
            bt = []
            for x in range(4):
                rt = []
                for y in range(4):
                    rt.append(cnt)
                    cnt += 1
                bt.append(rt)
            board.append(bt)
        return board

    def get_moves_by_combination(self, player):
        """Retrieve moves for a player that are in winning combinations.

        Args:
            player (str): Player to retrieve partially winning moves of.

        Returns:
            List of partial (or full) winning combinations for the player.
        """
        moves = []
        for combo in self.winning_combos:
            move = []
            for cell in combo:
                b, r, c = self.find(self.board, cell)
                if self.board[b][r][c] == player:
                    move += [cell]
            moves += [move]
        return moves

    def get_moves(self, player):
        """Get the previously made moves for the player.

        Args:
            player (str): Player to retrieve moves of.

        Returns:
            List of the available moves of a player.
        """
        moves = []
        cnt = 0
        for i in range(4):
            for x in range(4):
                for y in range(4):
                    if self.board[i][x][y] == player:
                        moves += [cnt]
                    cnt += 1
        return moves

    def available_combos(self, player):
        """Get the list of available moves and previously made moves.

        Args:
            player (str): Player to find combinations of.

        Returns:
            List of available moves and winning combinations.
        """
        return list(self.allowed_moves) + self.get_moves(player)

    @property
    def complete(self):
        """bool: Whether or not the game is finished or tied."""
        for player in self.players:
            for combo in self.winning_combos:
                combo_avail = True
                for pos in combo:
                    if pos not in self.available_combos(player):
                        combo_avail = False
                if combo_avail:
                    return self.winner is not None
        return True

    @property
    def winning_combo(self):
        """List[int]: List of the winning positions if the game is over."""
        if self.winner:
            positions = self.get_moves(self.winner)
            for combo in self.winning_combos:
                winner = combo
                for pos in combo:
                    if pos not in positions:
                        winner = None
                if winner:
                    return winner
        return None

    @property
    def winner(self):
        """str: The winning player if the game is over."""
        for player in self.players:
            positions = self.get_moves(player)
            for combo in self.winning_combos:
                won = True
                for pos in combo:
                    if pos not in positions:
                        won = False
                if won:
                    return player
        return None

    @property
    def ai_won(self):
        """bool: Whether or not the AI is the winner."""
        return self.winner == self.ai

    @property
    def human_won(self):
        """bool: Whether or not the Human is the winner."""
        return self.winner == self.human

    @property
    def tied(self):
        """bool: Whether or not the game ended in a tie."""
        return self.complete and self.winner is None

    @property
    def simple_heuristic(self):
        """int: Number of spaces available to win for the AI with the number
        of spaces available for the Human to win subtracted. Higher numbers
        are more favorable for the AI."""
        return self.check_available(self.ai) - self.check_available(self.human)

    def find_value(self, key):
        """Retrieve the value of the given position.

        Args:
            key (int): Position to find.

        Returns:
            The value at the given location on the board.
        """
        b, r, c = self.find(self.board, key)
        return self.board[b][r][c]

    def check_available(self, player):
        """int: Check the number of available wins on the current board
        state."""
        enemy = self.get_enemy(player)
        wins = 0
        for combo in self.winning_combos:
            if all([self.find_value(x) == player or \
                    self.find_value(x) != enemy for x in combo]):
                    wins += 1
        return wins

    def humans_move(self, move):
        """bool: Whether or not the move was successful or the move isn't
        possible."""
        if move not in self.allowed_moves:
            return False
        else:
            self.move(move, self.human)
            self.human_turn = False
            return True

    def spatial_heuristic(self):
        """Evaluate the board based on spatial patterns and configurations.

        Returns:
            int: Heuristic value indicating the desirability of the current state for the AI.
        """
        ai_wins = self.check_available(self.ai)
        human_wins = self.check_available(self.human)
        return ai_wins - human_wins
    def computers_move(self):
        """Initiates the process of attempting to find the best (or decent)
        move possible from the available positions on the board."""
        best_score = -1000
        best_move = None
        h = None
        win = False

        for move in self.allowed_moves:
            self.move(move, self.ai)
            if self.complete:
                win = True
                break
            else:
                h = self.think_ahead(self.human, -1000, 1000)
                self.depth_count = 0
                if h >= best_score:
                    best_score = h
                    best_move = move
                self.undo_move(move)

                # Check if it blocks the player
                self.move(move, self.human)
                if self.complete and self.winner == self.human:
                    if 1001 >= best_score:
                        best_score = 1001
                        best_move = move
                self.undo_move(move)

        if not win:
            self.move(best_move, self.ai)
        self.human_turn = True

    def think_ahead(self, player, a, b):
        if self.depth_count == self.difficulty or self.complete:
            return self.spatial_heuristic()  # Use the heuristic at a specific depth or terminal states
        if self.depth_count <= self.difficulty:
            self.depth_count += 1
            if player == self.ai:
                best_score = -1000
                for move in self.allowed_moves:
                    self.move(move, player)
                    score = self.think_ahead(self.get_enemy(player), a, b)
                    self.undo_move(move)
                    best_score = max(best_score, score)
                    a = max(a, best_score)
                    if a >= b:
                        break
                return best_score
            else:
                best_score = 1000
                for move in self.allowed_moves:
                    self.move(move, player)
                    score = self.think_ahead(self.get_enemy(player), a, b)
                    self.undo_move(move)
                    best_score = min(best_score, score)
                    b = min(b, best_score)
                    if a >= b:
                        break
                return best_score
        else:
            return self.spatial_heuristic()

    def undo_move(self, position):
        """Reverses a move."""
        self.allowed_moves += [position]
        self.allowed_moves.sort()
        i, x, y = self.find(self.board, position)
        self.board[i][x][y] = position

    def move(self, position, player):
        """Initiates a move on the given position.

        Args:
            position (int): Position on board to replace.
            player (str): Player to set piece to.
        """
        self.allowed_moves.remove(position)
        self.allowed_moves.sort()
        i, x, y = self.find(self.board, position)
        self.board[i][x][y] = player

    def get_enemy(self, player):
        """Returns the enemy of the player provided.

        Args:
            player (str): Player to get enemy of.
        """
        if player == self.human:
            return self.ai
        else:
            return self.human




