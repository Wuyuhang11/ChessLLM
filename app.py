import time
from prompt import get_player_prompt, get_referee_prompt,format_board
from api_client import APIClient
from game_engine import GameEngine

def main():
    game = GameEngine()
    providers = {'R': 'Qwen', 'B': 'DeepSeek'}
    
    while True:
        # 切换玩家
        side = game.current_player
        print(f"\n=== {providers[side]} ({'红方' if side == 'R' else '黑方'}) 的回合 ===")
        
        # 生成提示词
        prompt = get_player_prompt(side, game.board)
        move = None
        print(prompt)
        
        # 获取合法移动
        while True:
            # 调用API获取移动
            move = APIClient.get_move(providers[side], prompt)
            if not move:
                print("获取移动失败，正在重试...")
                time.sleep(1)
                continue
                
            # 验证移动格式
            piece, pos = move
            if piece[0] != side or not (0 <= pos[0] <= 9) or not (0 <= pos[1] <= 8):
                print("移动格式错误，正在重试...")
                continue
                
            # 裁判验证
            start_pos = game.history[piece][-1]
            referee_prompt = get_referee_prompt((piece, start_pos, pos), game.board)
            if APIClient.judge_move(referee_prompt):
                break
                
            print("非法移动，要求重新下棋...")
            game.rollback_move(move)
            prompt += "\n（你上次的移动被判定为非法，请仔细检查规则后重新下棋）"
        
        # 应用移动
        result = game.apply_move(move)
        print(f"移动成功：{move}")
        print(f"当前棋盘：\n{format_board(game.board)}")
        
        # 检查游戏结束
        if result == 'game_over' or game.check_game_over():
            winner = '红方' if game.scores['R'] > game.scores['B'] else '黑方'
            print(f"\n游戏结束！胜利方：{winner}")
            print(f"最终比分：红方 {game.scores['R']} - 黑方 {game.scores['B']}")
            break
            
        # 切换玩家
        game.current_player = 'B' if side == 'R' else 'R'

if __name__ == "__main__":
    main()