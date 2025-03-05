# API配置
API_KEY = "sk-kifqepgmrmlstabhxlmxrylkppvcppumtvwcdbwajgotuvvk"
DASHSCOPE_API_KEY = "sk-6fc987d8a545464e95fb35ed3ae85d53"

API_CONFIG = {
    "Qwen": {
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    },
    "DeepSeek1": {
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "deepseek-ai/DeepSeek-R1",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    },
    "DeepSeek2": {
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "deepseek-ai/DeepSeek-R1",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    },
    "internlm": {
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "internlm/internlm2_5-20b-chat",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    },
    "QwenMax": {  # 新增 qwen-plus 配置
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model": "qwen-max",
        "headers": {
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
            "Content-Type": "application/json",
        },
    },
}

# 初始棋盘配置
INIT_BOARD = [
    ["BC1", "BM1", "BX1", "BS1", "BK", "BS2", "BX2", "BM2", "BC2"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "BP1", "--", "--", "--", "--", "--", "BP2", "--"],
    ["BZ1", "--", "BZ2", "--", "BZ3", "--", "BZ4", "--", "BZ5"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["RB1", "--", "RB2", "--", "RB3", "--", "RB4", "--", "RB5"],
    ["--", "RP1", "--", "--", "--", "--", "--", "RP2", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["RC1", "RM1", "RX1", "RS1", "RK", "RS2", "RX2", "RM2", "RC2"],
]

# 棋子类型映射
PIECE_MAP = {
    "R": "红方",
    "B": "黑方",
    "RC1": "红车1",
    "RC2": "红车2",
    "RM1": "红马1",
    "RM2": "红马2",
    "RX1": "红象1",
    "RX2": "红象2",
    "RS1": "红士1",
    "RS2": "红士2",
    "RP1": "红炮1",
    "RP2": "红炮2",
    "RB1": "红兵1",
    "RB2": "红兵2",
    "RB3": "红兵3",
    "RB4": "红兵4",
    "RB5": "红兵5",
    "RK": "红将",
    "BC1": "黑车1",
    "BC2": "黑车2",
    "BM1": "黑马1",
    "BM2": "黑马2",
    "BX1": "黑象1",
    "BX2": "黑象2",
    "BS1": "黑士1",
    "BS2": "黑士2",
    "BP1": "黑炮1",
    "BP2": "黑炮2",
    "BZ1": "黑卒1",
    "BZ2": "黑卒2",
    "BZ3": "黑卒3",
    "BZ4": "黑卒4",
    "BZ5": "黑卒5",
    "BK": "黑将",
}


PIECE_SCORE = {
    "RC1": 9, "RC2": 9, "BC1": 9, "BC2": 9,  # 车
    "RM1": 4, "RM2": 4, "BM1": 4, "BM2": 4,  # 马
    "RP1": 4.5, "RP2": 4.5, "BP1": 4.5, "BP2": 4.5,  # 炮
    "RB1": 1, "RB2": 1, "RB3": 1, "RB4": 1, "RB5": 1,  # 红兵
    "BZ1": 1, "BZ2": 1, "BZ3": 1, "BZ4": 1, "BZ5": 1,  # 黑卒
    "RX1": 2, "RX2": 2, "BX1": 2, "BX2": 2,  # 象
    "RS1": 2, "RS2": 2, "BS1": 2, "BS2": 2,  # 士
    "RK": 100, "BK": 100  # 将军设为高分，确保吃掉对方将军直接获胜
}