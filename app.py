import time
from prompt import get_player_prompt, get_referee_prompt, get_rollback_prompt, format_board
from api_client import APIClient
from game_engine import GameEngine

def log_to_file(filename, round_count, side, move, board, scores, rollback_info=None):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"回合 {round_count} ({'红方' if side == 'R' else '黑方'}):\n")
        f.write(f"移动: {move}\n")
        f.write(f"棋盘:\n{format_board(board)}\n")
        f.write(f"分数: 红方 {scores['R']} - 黑方 {scores['B']}\n")
        if rollback_info:
            f.write(f"回滚信息:\n{rollback_info}\n")
        f.write("-" * 50 + "\n")

def main():
    global game  # 使 game 在 get_rollback_prompt 中可访问
    game = GameEngine()
    providers = {'R': 'DeepSeek1', 'B': 'DeepSeek2'}
    round_count = 0
    log_file = "chess_game_log.txt"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("象棋对战日志\n")
        f.write(f"初始棋盘:\n{format_board(game.board)}\n")
        f.write("-" * 50 + "\n")
    
    while True:
        round_count += 1
        side = game.current_player
        print(f"\n=== {providers[side]} ({'红方' if side == 'R' else '黑方'}) 的回合 ===")
        prompt = get_player_prompt(side, game.board)
        print(prompt)
        
        # 获取移动
        move = None
        max_retries = 3
        for attempt in range(max_retries):
            move = APIClient.get_move(providers[side], prompt)
            if move:
                break
            print(f"获取移动失败，第 {attempt + 1}/{max_retries} 次重试...")
            time.sleep(2)
        if not move:
            print(f"经过 {max_retries} 次尝试仍失败，跳过此回合")
            game.current_player = 'B' if side == 'R' else 'R'
            continue
        
        piece, pos = move
        if piece[0] != side or not (0 <= pos[0] <= 9) or not (0 <= pos[1] <= 8):
            print(f"移动格式错误或棋子 {piece} 不属于 {side} 方，跳过此回合")
            continue
        
        # 检查棋子是否存在
        if not game.history.get(piece):
            print(f"错误：棋子 {piece} 不存在于棋盘上，跳过此回合")
            continue
        
        # 裁判验证
        start_pos = game.history[piece][-1]
        referee_prompt = get_referee_prompt((piece, start_pos, pos), game.board)
        if not APIClient.judge_move(referee_prompt):
            # 回滚并生成反馈
            game.rollback_move(move)
            reason = "裁判判定为非法移动（可能违反路径规则、目标规则或边界条件）"
            rollback_prompt = get_rollback_prompt(side, move, game.board, reason)
            print("非法移动，回滚并生成反馈...")
            print(rollback_prompt)
            # 调用 API 获取回滚分析（可选）
            rollback_info = "待模型分析"  # 可替换为 API 调用结果
            log_to_file(log_file, round_count, side, move, game.board, game.scores, rollback_info)
            continue
        
        # 应用移动
        result = game.apply_move(move)
        if not result:
            print(f"移动 {move} 应用失败，跳过此回合")
            continue
        
        print(f"移动成功：{move}")
        print(f"当前棋盘：\n{format_board(game.board)}")
        print(f"当前分数：红方 {game.scores['R']} - 黑方 {game.scores['B']}")
        log_to_file(log_file, round_count, side, move, game.board, game.scores)
        
        if result == 'game_over' or game.check_game_over():
            winner = '红方' if game.scores['R'] > game.scores['B'] else '黑方'
            print(f"\n游戏结束！胜利方：{winner}")
            break
        elif round_count >= 50:
            winner = '红方' if game.scores['R'] > game.scores['B'] else '黑方'
            print(f"\n50回合结束！胜利方：{winner}")
            break
        game.current_player = 'B' if side == 'R' else 'R'

if __name__ == "__main__":
    main()