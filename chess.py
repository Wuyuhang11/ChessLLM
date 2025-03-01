from app import INIT_BOARD


# 初始化棋盘
board = INIT_BOARD

# 打印棋盘
for row in board:
    print(" ".join(row))
