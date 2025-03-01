from config import PIECE_MAP

def get_player_prompt(side: str, board: list) -> str:
    """生成玩家提示词"""
    role = "红方" if side == "R" else "黑方"
    return f'''
    你正在参与中国象棋对战，当前为{role}。棋盘状态如下：
    {format_board(board)}

    棋子代码规则（第一个字母表示阵营，第二个字母表示兵种，第三个代表第几个）：
    R-红方，B-黑方
    K-将/帅，S-士，X-象，M-马，C-车，P-炮，B-兵/卒
    RS1-红士1, BS1-黑士1，RB-红兵2，RK-红将，BK-黑将

    移动规则：
    1. 将/帅：只能在九宫格内移动，每次一步
    2. 士：斜线移动，只能在九宫格内
    3. 象：走"田"字，不能过河，被塞象眼不能走
    4. 马：走"日"字，被蹩马腿不能走
    5. 车：直线任意距离
    6. 炮：移动时需隔一子才能吃子
    7. 兵：过河前只能前进，过河后可左右移动
    
    吃子规则：
    1. 当你的棋子移动到对方棋子的位置时，会吃掉对方的棋子。
    2. 吃子时，目标位置必须是对方的棋子。
    3. 吃子后，目标位置的棋子会被替换为你的棋子，原位置变为空。
    
    请严格按照以下格式返回移动指令：[棋子代码,[目标行,目标列]]
    示例：["{'R' if side == 'R' else 'B'}C", [4, 5]]
    只需返回JSON格式，不要包含其他内容！
    '''

def get_referee_prompt(move: tuple, board: list) -> str:
    """生成裁判提示词"""
    piece, start_pos, end_pos = move
    return f'''
    请严格根据中国象棋规则判断此移动是否合法：
    
    移动棋子：{PIECE_MAP[piece[0]]}{PIECE_MAP[piece[1]]}
    起始位置：行{start_pos[0]+1}列{start_pos[1]+1}
    目标位置：行{end_pos[0]+1}列{end_pos[1]+1}
    
    当前棋盘状态：
    {format_board(board)}
    
    请检查：
    1. 是否符合该棋子的基本走法
    2. 是否违反特殊规则（马腿、象眼、炮架等）
    3. 是否超出棋盘范围
    4. 是否吃己方棋子
    
    只返回单个数字：
    1-合法，0-非法
    不要包含其他任何内容！
    '''

def format_board(board: list) -> str:
    """格式化棋盘为可视字符串"""
    return '\n'.join([' '.join(row) for row in board])