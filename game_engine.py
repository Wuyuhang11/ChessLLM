from collections import defaultdict
from config import INIT_BOARD

class GameEngine:
    def __init__(self):
        self.board = [row.copy() for row in INIT_BOARD]
        self.history = defaultdict(list)
        self.scores = {'R': 0, 'B': 0}
        self.current_player = 'R'
        
        # 初始化历史记录
        for i in range(10):
            for j in range(9):
                piece = self.board[i][j]
                if piece != '--':
                    self.history[piece].append((i, j))

    def apply_move(self, move: tuple) -> bool:
        """应用移动并更新棋盘"""
        piece, (new_row, new_col) = move
        
        # 查找原位置
        if not self.history[piece]:
            return False
        old_row, old_col = self.history[piece][-1]
        
        # 检查目标位置
        target = self.board[new_row][new_col]
        if target.startswith(piece[0]):
            return False  # 不能吃己方棋子
        
        # 更新棋盘
        self.board[old_row][old_col] = '--'
        self.board[new_row][new_col] = piece
        self.history[piece].append((new_row, new_col))
        
        # 处理被吃掉的棋子
        if target != '--':
            self.history[target].pop()
            if 'K' in target:  # 将军被吃
                self.scores['R' if piece[0] == 'R' else 'B'] += 1
                return 'game_over'
        return True

    def rollback_move(self, move: tuple):
        """回滚非法移动"""
        piece, (new_row, new_col) = move
        if len(self.history[piece]) < 2:
            return
        
        # 恢复原位置
        self.history[piece].pop()
        old_row, old_col = self.history[piece][-1]
        self.board[new_row][new_col] = '--'
        self.board[old_row][old_col] = piece

    def check_game_over(self):
        """检查游戏是否结束"""
        return any(piece.endswith('K') and len(self.history[piece]) == 0 
                for piece in ['RK', 'BK'])