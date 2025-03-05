from collections import defaultdict
from config import INIT_BOARD, PIECE_SCORE

class GameEngine:
    def __init__(self):
        self.board = [row.copy() for row in INIT_BOARD]
        self.history = defaultdict(list)
        self.scores = {'R': 0, 'B': 0}
        self.current_player = 'R'
        self.last_eaten = None
        
        # 初始化历史记录并验证
        for i in range(10):
            for j in range(9):
                piece = self.board[i][j]
                if piece != '--':
                    self.history[piece].append((i, j))
        # 调试：打印初始历史记录
        print("初始历史记录:", dict(self.history))

    def apply_move(self, move: tuple) -> bool:
        piece, (new_row, new_col) = move
        
        # 检查棋子是否存在于历史记录中
        if not self.history[piece]:
            print(f"错误：棋子 {piece} 不存在于历史记录中")
            return False
        
        old_row, old_col = self.history[piece][-1]
        target = self.board[new_row][new_col]
        if target.startswith(piece[0]):
            print(f"错误：不能吃己方棋子 {target}")
            return False
        
        self.board[old_row][old_col] = '--'
        self.board[new_row][new_col] = piece
        self.history[piece].append((new_row, new_col))
        self.last_eaten = None
        
        if target != '--':
            self.last_eaten = (target, new_row, new_col)
            self.history[target].pop()
            self.scores[piece[0]] += PIECE_SCORE.get(target, 0)
            if 'K' in target:
                return 'game_over'
        return True

    def rollback_move(self, move: tuple):
        piece, (new_row, new_col) = move
        if len(self.history[piece]) < 2:
            return
        
        self.history[piece].pop()
        old_row, old_col = self.history[piece][-1]
        self.board[new_row][new_col] = '--'
        self.board[old_row][old_col] = piece
        if self.last_eaten:
            target, row, col = self.last_eaten
            self.board[row][col] = target
            self.history[target].append((row, col))
            self.scores[piece[0]] -= PIECE_SCORE.get(target, 0)
            
    def check_game_over(self):
        """检查游戏是否结束"""
        return any(
            piece.endswith("K") and len(self.history[piece]) == 0
            for piece in ["RK", "BK"]
        )