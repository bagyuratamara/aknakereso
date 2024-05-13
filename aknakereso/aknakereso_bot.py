import numpy as np

class MinesweeperGame:
    def __init__(self, size=10, bomb_number=10):
        self.size = size
        self.bomb_number = bomb_number
        self.np_random = np.random.RandomState()
        self.reset()

    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.revealed = np.zeros((self.size, self.size), dtype=bool)
        self.flags = np.zeros((self.size, self.size), dtype=bool)
        self.game_over = False
        self.win = False
        self.first_click = None
        self.active_bombs = self.bomb_number
        self._place_bombs()
        self.reward = 0
        return self.get_state()

    def _place_bombs(self):
        bomb_positions = set()
        exclude_cells = self._cells_around_first_click() 
        while len(bomb_positions) < self.bomb_number:
            x = self.np_random.randint(0, self.size)
            y = self.np_random.randint(0, self.size)
            if (x, y) not in exclude_cells:
                bomb_positions.add((x, y))
        for pos in bomb_positions:
            self.board[pos] = -1
        self._calculate_adjacent_numbers()

    def _cells_around_first_click(self):
        if self.first_click is None:
            return set()
        x, y = self.first_click
        cells = set()
        for i in range(max(0, x-1), min(x+2, self.size)):
            for j in range(max(0, y-1), min(y+2, self.size)):
                cells.add((i, j))
        return cells


    def _is_near_first_click(self, x, y):
        if self.first_click is None:
            return False
        first_x, first_y = self.first_click
        return max(abs(first_x - x), abs(first_y - y)) <= 1

    def _calculate_adjacent_numbers(self):
        for (x, y), value in np.ndenumerate(self.board):
            if value == -1:
                continue
            adj_bombs = sum(
                self.board[i, j] == -1
                for i in range(max(0, x-1), min(x+2, self.size))
                for j in range(max(0, y-1), min(y+2, self.size))
            )
            self.board[x, y] = adj_bombs

    def step(self, action):
        if isinstance(action, tuple):
            action_type, x, y = action
        else:
            action_type, x, y = self.convert_action(action)

        if self.revealed[x, y]:
            reward = 0
        elif action_type == 'reveal':
            reward = self.reveal(x, y)
        elif action_type == 'flag':
            reward = self.toggle_flag(x, y)

        done = self.game_over or self.win
        next_state = self.get_state()
        return next_state, reward, done

    def get_state(self):
        visible_board = np.copy(self.board)
        visible_board[~self.revealed] = 0
        return visible_board.flatten()

    def reveal(self, x, y):
        if self.game_over:
            return 0
        if self.first_click is None:
            self.first_click = (x, y)
            self._place_bombs()
            self._calculate_adjacent_numbers()  

        if self.revealed[x, y] or self.flags[x, y]:
            return 0

        self.revealed[x, y] = True
        if self.board[x, y] == -1:
            self.game_over = True
            return -self.active_bombs
        else:
            all_neighbors_hidden = all(
                not self.revealed[i, j]
                for i in range(max(0, x-1), min(x+2, self.size))
                for j in range(max(0, y-1), min(y+2, self.size))
                if (i, j) != (x, y)
            )
            reward = -1 if all_neighbors_hidden else 0 
        

        if self.board[x, y] == 0:
            for i in range(max(0, x-1), min(x+2, self.size)):
                for j in range(max(0, y-1), min(y+2, self.size)):
                    if not self.revealed[i, j]:
                        self.reveal(i, j) 

        self.check_win()
        return reward

    def toggle_flag(self, x, y):
        if not self.revealed[x, y] and not self.game_over:
            self.flags[x, y] = not self.flags[x, y]
            if self.board[x, y] == -1:
                self.active_bombs += -1 if self.flags[x, y] else 1
                return 1 if self.flags[x, y] else -1
        self.check_win()
        return 0

    def check_win(self):
        if np.all(self.revealed | (self.board == -1) == True):
            self.win = True
            self.game_over = True
            self.active_bombs = 0  
            return 15
        
    def seed(self, seed=None):
        self.np_random.seed(seed)
    
    def convert_action(self, action_index):
        action_type = 'reveal' if action_index % 2 == 0 else 'flag'
        x = (action_index // 2) // self.size
        y = (action_index // 2) % self.size
        return (action_type, x, y)