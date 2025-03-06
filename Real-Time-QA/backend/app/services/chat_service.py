"""
Dify Chat Service

Provides functionality for communicating with the Dify API, supporting chat completion and streaming responses.
Uses semaphores to control concurrent request count to avoid overload.
"""
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from app.core.config import settings
from app.utils.logger import get_logger
import time

# Get logger
logger = get_logger("chat_service")

class ChatService:
    """
    Dify Chat Service Class
    
    Responsible for communicating with the Dify API, handling chat requests and responses.
    Supports concurrency control to limit the number of simultaneous requests.
    """
    
    def __init__(self, max_concurrent_requests: int = 10):
        """
        Initialize chat service
        
        Args:
            max_concurrent_requests: Maximum concurrent requests, default is 10
        """
        self.api_key = settings.DIFY_API_KEY
        self.api_url = settings.DIFY_API_URL
        
        # Limit concurrent requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to the Dify API
        
        Args:
            messages: List of message objects with role and content
            temperature: Sampling temperature, controls randomness
            max_tokens: Maximum tokens in the response
            stream: Whether to stream the response
            max_retries: Maximum number of retry attempts
            
        Returns:
            Response from the Dify API
        """
        # Use mock response in mock mode
        if settings.MOCK_MODE:
            logger.info("Using mock response in mock mode")
            return self.get_mock_response(messages[-1]["content"])
        
        # Use semaphore to limit concurrent requests
        async with self.semaphore:
            retry_count = 0
            
            while retry_count <= max_retries:
                try:
                    start_time = time.time()
                    logger.info(f"Sending request to Dify API: tokens={max_tokens}")
                    
                    # 准备请求数据
                    # 将 OpenAI 格式的消息转换为 Dify 格式
                    dify_messages = []
                    for msg in messages:
                        dify_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    request_data = {
                        "inputs": {},
                        "query": messages[-1]["content"] if messages else "",
                        "response_mode": "streaming" if stream else "blocking",
                        "conversation_id": None,  # 可以添加会话ID支持
                        "user": "user",  # 可以从请求中获取用户ID
                        "stream": stream,
                        "model_config": {
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                    }
                    
                    # 如果有历史消息，添加到请求中
                    if len(messages) > 1:
                        history = []
                        for i in range(0, len(messages) - 1, 2):
                            if i + 1 < len(messages):
                                history.append({
                                    "user": messages[i]["content"],
                                    "assistant": messages[i + 1]["content"]
                                })
                        request_data["history"] = history
                    
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    # 发送请求
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            f"{self.api_url}/chat-messages",
                            json=request_data,
                            headers=headers
                        ) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise Exception(f"Dify API returned error: {response.status}, {error_text}")
                            
                            if stream:
                                return response  # 返回响应对象以便流式处理
                            else:
                                result = await response.json()
                    
                    elapsed_time = time.time() - start_time
                    logger.info(f"Dify API response received in {elapsed_time:.2f}s")
                    
                    # 处理并返回响应
                    if not stream:
                        return {
                            "id": result.get("conversation_id", "unknown"),
                            "model": result.get("model", "dify-model"),
                            "content": result.get("answer", ""),
                            "role": "assistant",
                            "finish_reason": "stop",
                            "usage": {
                                "prompt_tokens": result.get("metadata", {}).get("prompt_tokens", 0),
                                "completion_tokens": result.get("metadata", {}).get("completion_tokens", 0),
                                "total_tokens": result.get("metadata", {}).get("total_tokens", 0)
                            }
                        }
                
                except Exception as e:
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    
                    if retry_count <= max_retries:
                        logger.warning(f"Dify API request failed (attempt {retry_count}/{max_retries}): {str(e)}")
                        logger.warning(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Dify API request failed after {max_retries} retries: {str(e)}")
                        raise Exception(f"Failed to get response from Dify API: {str(e)}")
    
    def get_mock_response(self, question: str) -> Dict[str, Any]:
        """
        Generate a mock response for testing without calling the actual API
        
        Args:
            question: The user's question
            
        Returns:
            A mock response object
        """
        logger.info(f"Generating mock response for question: {question[:50]}...")
        
        # Simple mock response
        mock_content = f"This is a mock response to your question: '{question}'. In mock mode, the actual API will not be called."
        
        return {
            "id": "mock-response-id",
            "model": "mock-model",
            "content": mock_content,
            "role": "assistant",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": len(question) // 4,
                "completion_tokens": len(mock_content) // 4,
                "total_tokens": (len(question) + len(mock_content)) // 4
            }
        }

# Create global chat service instance
chat_service = ChatService() 