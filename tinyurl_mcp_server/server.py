import os
import logging
import requests
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """从环境变量获取TinyURL API密钥"""
    api_key = os.getenv("TINYURL_API_KEY")
    if not api_key:
        raise ValueError("TINYURL_API_KEY环境变量必须设置")
    return api_key

# 初始化FastMCP
mcp = FastMCP("tinyurl")

@mcp.tool()
def create_short_url(url: str) -> Dict[str, Any]:
    """
    将长URL转换为短链接
    
    参数:
    - url: 需要缩短的URL
    
    返回:
    - 包含短链接信息的字典
    """
    try:
        api_key = get_api_key()
        endpoint = f"https://api.tinyurl.com/create?api_token={api_key}"
        
        # 准备请求参数
        payload = {"url": url}
        
        # 设置请求头
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        
        # 发送API请求
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        # 返回API响应
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {str(e)}")
        return {"error": f"无法创建短链接: {str(e)}"}
    except ValueError as e:
        logger.error(f"配置错误: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return {"error": f"创建短链接时发生错误: {str(e)}"}

def main():
    """启动MCP服务器"""
    logger.info("启动TinyURL MCP服务...")
    mcp.run()

if __name__ == "__main__":
    main()