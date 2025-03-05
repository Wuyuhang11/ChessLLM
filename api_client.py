from openai import OpenAI
from config import API_CONFIG
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re
import time

class APIClient:
    @staticmethod
    def get_move(provider: str, prompt: str) -> tuple:
        """
        获取棋子移动指令，支持 qwen-max 的流式响应和其他模型的普通请求。
        重试次数：5 次，每次超时 60 秒。
        """
        config = API_CONFIG[provider]
        
        # 为普通请求创建带有重试机制的会话
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # 总尝试次数（包括初次请求）为 5
            backoff_factor=2,  # 重试间隔因子，2秒、4秒、8秒、16秒、32秒
            status_forcelist=[500, 502, 503, 504],  # 重试的 HTTP 状态码
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        if provider == "qwen-max":
            # qwen-max 使用 OpenAI 客户端的流式请求
            client = OpenAI(
                api_key=config["headers"]["Authorization"].split("Bearer ")[1],
                base_url=config["url"]
            )
            for attempt in range(5):  # 手动实现 5 次重试
                try:
                    completion = client.chat.completions.create(
                        model=config["model"],
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=512,
                        stream=True
                    )
                    content = ""
                    for chunk in completion:
                        if chunk.choices[0].delta.content:
                            content += chunk.choices[0].delta.content
                    break  # 成功获取响应，跳出重试循环
                except Exception as e:
                    print(f"qwen-max API 调用失败，第 {attempt + 1}/5 次重试: {e}")
                    if attempt < 4:  # 不是最后一次尝试
                        time.sleep(2 ** attempt * 2)  # 指数退避：2、4、8、16 秒
                    else:
                        print("qwen-max 重试 5 次仍失败，返回 None")
                        return None
        else:
            # 其他模型使用 requests 的 POST 请求
            payload = {
                "model": config["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 512
            }
            try:
                response = session.post(
                    url=config["url"],
                    headers=config["headers"],
                    json=payload,
                    timeout=60  # 超时时间设置为 60 秒
                )
                response.raise_for_status()
                content = response.json()['choices'][0]['message']['content']
            except requests.exceptions.RequestException as e:
                print(f"API 调用失败，经过 5 次重试仍未成功: {e}")
                return None

        # 解析移动指令
        pattern = r'移动指令\s*\n\["([A-Z]{2}\d)",\s*\[(\d+),\s*(\d+)\]\]'
        match = re.search(pattern, content)
        if match:
            piece = match.group(1)
            row = int(match.group(2))
            col = int(match.group(3))
            return (piece, (row, col))
        print(f"正则匹配失败，content: {content}")
        return None

    @staticmethod
    def judge_move(prompt: str) -> bool:
        """
        调用裁判 API 判断移动合法性。
        重试次数：5 次，每次超时 60 秒。
        """
        config = API_CONFIG["internlm"]
        payload = {
            "model": config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 1
        }

        # 创建带有重试机制的会话
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # 总尝试次数为 5
            backoff_factor=2,  # 重试间隔因子，2秒、4秒、8秒、16秒、32秒
            status_forcelist=[500, 502, 503, 504],  # 重试的 HTTP 状态码
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        try:
            response = session.post(
                url=config["url"],
                headers=config["headers"],
                json=payload,
                timeout=60  # 超时时间设置为 60 秒
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content'].strip()
            return result == '1'
        except requests.exceptions.RequestException as e:
            print(f"裁判 API 调用失败，经过 5 次重试仍未成功: {e}")
            return False
