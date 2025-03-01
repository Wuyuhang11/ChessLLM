import requests
import re
import json
from config import API_CONFIG

class APIClient:
    @staticmethod
    def get_move(provider: str, prompt: str) -> tuple:
        """调用大模型API获取移动指令"""
        config = API_CONFIG[provider]
        payload = {
            "model": config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 512
        }
        
        try:
            response = requests.post(
                url=config["url"],
                headers=config["headers"],
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            # 使用正则提取移动指令
            content = response.json()['choices'][0]['message']['content']
            pattern = r'\["([A-Z]{2})",\s*\[(\d+),\s*(\d+)\]\]'
            match = re.search(pattern, content)
            
            if match:
                piece = match.group(1)
                row = int(match.group(2))
                col = int(match.group(3))
                return (piece, (row, col))
            return None
        except Exception as e:
            print(f"API请求失败：{str(e)}")
            return None

    @staticmethod
    def judge_move(prompt: str) -> bool:
        """调用裁判API判断移动合法性"""
        config = API_CONFIG["Kimi"]
        payload = {
            "model": config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 1
        }
        
        try:
            response = requests.post(
                url=config["url"],
                headers=config["headers"],
                json=payload,
                timeout=30
            )
            result = response.json()['choices'][0]['message']['content'].strip()
            return result == '1'
        except:
            return False