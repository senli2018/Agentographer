"""
WebSocket Chat Service

Provides WebSocket connection management, message processing, and communication with DIFY API.
Each client is identified by a unique ID, supporting point-to-point communication.
"""
from typing import Dict, List, Any, Optional
import json
import asyncio
import time
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from app.services.chat_service import chat_service
from app.core.config import settings
from app.utils.logger import get_logger
from app.utils.text_utils import clean_text

# Get logger
logger = get_logger("websocket_service")

class ConnectionManager:
    """
    WebSocket Connection Manager
    
    Responsible for managing WebSocket connections, processing messages, and communicating with DIFY API.
    Each connection has a unique client ID, supporting concurrent processing of multiple client requests.
    """
    
    def __init__(self):
        """Initialize connection manager"""
        # Active connections dictionary, key is client ID, value is WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}
        # Tasks in process, key is client ID, value is task
        self.tasks: Dict[str, asyncio.Task] = {}
        # Heartbeat tasks, key is client ID, value is task
        self.heartbeat_tasks: Dict[str, asyncio.Task] = {}
        # Last activity time, key is client ID, value is timestamp
        self.last_activity: Dict[str, float] = {}
        # Heartbeat interval (seconds)
        self.heartbeat_interval = settings.WEBSOCKET_HEARTBEAT_INTERVAL
        # Heartbeat timeout (seconds)
        self.heartbeat_timeout = settings.WEBSOCKET_HEARTBEAT_TIMEOUT
        # Mock mode
        self.mock_mode = settings.MOCK_MODE
        
        if self.mock_mode:
            logger.warning("WebSocket service is running in mock mode, will not call actual DIFY API")
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """
        Connect a new client
        
        Args:
            websocket: WebSocket connection
            client_id: Client ID
        """
        try:
            # Check if client ID already exists
            if not hasattr(websocket, "client_state") or websocket.client_state != WebSocketState.CONNECTED:
                logger.error(f"WebSocket connection not accepted: client_id={client_id}")
                raise RuntimeError("WebSocket is not connected. Need to call \"accept\" first.")
            
            # Clean up any existing old connections first
            if client_id in self.active_connections:
                logger.warning(f"Client ID already exists, disconnecting old connection: client_id={client_id}")
                await self.disconnect(client_id)
            
            # Register new connection
            self.active_connections[client_id] = websocket
            self.last_activity[client_id] = time.time()
            
            # Start heartbeat task
            self.heartbeat_tasks[client_id] = asyncio.create_task(
                self._heartbeat_loop(client_id)
            )
            
            # Send a test message to verify connection is normal
            try:
                await websocket.send_text(json.dumps({
                    "type": "system",
                    "content": "Connection established"
                }))
            except Exception as e:
                logger.error(f"Connection test failed, disconnecting: client_id={client_id}, error={str(e)}")
                await self.disconnect(client_id)
                return
            
            logger.info(f"Client connected: client_id={client_id}, total_connections={len(self.active_connections)}")
        
        except Exception as e:
            logger.error(f"Error connecting: client_id={client_id}, error={str(e)}")
            # Ensure resources are cleaned up
            await self.disconnect(client_id)
            # Re-raise exception for caller to handle
            raise
    
    async def disconnect(self, client_id: str):
        """
        Disconnect a client
        
        Args:
            client_id: Client ID to disconnect
        """
        # Cancel any running tasks for this client
        if client_id in self.tasks and not self.tasks[client_id].done():
            self.tasks[client_id].cancel()
            try:
                await self.tasks[client_id]
            except asyncio.CancelledError:
                pass
            del self.tasks[client_id]
        
        # Cancel heartbeat task
        if client_id in self.heartbeat_tasks and not self.heartbeat_tasks[client_id].done():
            self.heartbeat_tasks[client_id].cancel()
            try:
                await self.heartbeat_tasks[client_id]
            except asyncio.CancelledError:
                pass
            del self.heartbeat_tasks[client_id]
        
        # Remove from active connections
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client disconnected: client_id={client_id}, remaining_connections={len(self.active_connections)}")
        
        # Remove from last activity
        if client_id in self.last_activity:
            del self.last_activity[client_id]
    
    async def send_personal_message(self, message_data: Dict[str, Any], client_id: str):
        """
        Send a message to a specific client
        
        Args:
            message_data: Message data to send
            client_id: Client ID to send to
        """
        if client_id not in self.active_connections:
            logger.warning(f"Cannot send message, client not connected: client_id={client_id}")
            return
        
        # Update last activity time
        self.last_activity[client_id] = time.time()
        
        try:
            # Add timestamp if not present
            if "timestamp" not in message_data:
                message_data["timestamp"] = self.get_timestamp()
            
            # Convert to JSON and send
            message_json = json.dumps(message_data)
            await self.active_connections[client_id].send_text(message_json)
            
            # Log message type
            message_type = message_data.get("type", "unknown")
            if message_type == "chat":
                # For chat messages, log a preview of content
                content = message_data.get("content", "")
                preview = content[:50] + "..." if len(content) > 50 else content
                logger.debug(f"Sent chat message to client: client_id={client_id}, content_preview='{preview}'")
            else:
                # For other message types, just log the type
                logger.debug(f"Sent message to client: client_id={client_id}, type={message_type}")
                
        except Exception as e:
            logger.error(f"Error sending message to client: client_id={client_id}, error={str(e)}")
            # If connection is broken, disconnect the client
            if "connection is closed" in str(e).lower() or "not connected" in str(e).lower():
                logger.info(f"Connection closed, disconnecting client: client_id={client_id}")
                await self.disconnect(client_id)
    
    async def process_chat_message(self, client_id: str, content: str):
        """
        Process a chat message from a client
        
        Args:
            client_id: Client ID that sent the message
            content: Message content
        """
        # Clean the text
        cleaned_content = clean_text(content)
        if not cleaned_content:
            logger.warning(f"Empty message after cleaning: client_id={client_id}")
            await self.send_personal_message(
                {"type": "error", "content": "Message is empty after cleaning"},
                client_id
            )
            return
        
        # Update last activity time
        self.last_activity[client_id] = time.time()
        
        # Log the received message
        preview = cleaned_content[:50] + "..." if len(cleaned_content) > 50 else cleaned_content
        logger.info(f"Received chat message: client_id={client_id}, content_preview='{preview}'")
        
        # Echo the message back to the client
        await self.send_personal_message(
            {
                "type": "chat",
                "role": "user",
                "content": cleaned_content,
                "client_id": client_id
            },
            client_id
        )
        
        # Send typing indicator
        await self.send_personal_message(
            {"type": "typing", "status": True},
            client_id
        )
        
        # Process the message in a separate task
        if client_id in self.tasks and not self.tasks[client_id].done():
            # Cancel previous task if still running
            self.tasks[client_id].cancel()
            try:
                await self.tasks[client_id]
            except asyncio.CancelledError:
                pass
        
        # Create new task for handling the chat request
        self.tasks[client_id] = asyncio.create_task(
            self._handle_chat_request(client_id, cleaned_content)
        )
    
    async def _handle_chat_request(self, client_id: str, question: str):
        """
        Handle a chat request by sending it to the DIFY API
        
        Args:
            client_id: Client ID that sent the request
            question: Question to send to DIFY
        """
        try:
            # Create messages for DIFY
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
            
            # Call DIFY API
            logger.info(f"Sending request to DIFY API: client_id={client_id}")
            start_time = time.time()
            
            response = await chat_service.chat_completion(
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Received response from DIFY API: client_id={client_id}, time={elapsed_time:.2f}s")
            
            # Extract content from response
            content = response.get("content", "")
            if not content:
                logger.warning(f"Empty response from DIFY API: client_id={client_id}")
                content = "I'm sorry, I couldn't generate a response. Please try again."
            
            # Send response to client
            await self.send_personal_message(
                {
                    "type": "chat",
                    "role": "assistant",
                    "content": content,
                    "client_id": client_id
                },
                client_id
            )
            
        except Exception as e:
            logger.error(f"Error processing chat request: client_id={client_id}, error={str(e)}")
            
            # Send error message to client
            await self.send_personal_message(
                {
                    "type": "error",
                    "content": f"Error processing your request: {str(e)}",
                    "client_id": client_id
                },
                client_id
            )
            
        finally:
            # Stop typing indicator
            await self.send_personal_message(
                {"type": "typing", "status": False},
                client_id
            )
    
    async def heartbeat(self, client_id: str):
        """
        Send a heartbeat ping to a client
        
        Args:
            client_id: Client ID to send heartbeat to
        """
        if client_id not in self.active_connections:
            return
        
        try:
            await self.send_personal_message(
                {"type": "ping", "timestamp": self.get_timestamp()},
                client_id
            )
            logger.debug(f"Sent heartbeat ping: client_id={client_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending heartbeat: client_id={client_id}, error={str(e)}")
            return False
    
    async def _heartbeat_loop(self, client_id: str):
        """
        Heartbeat loop for a client
        
        Args:
            client_id: Client ID to monitor
        """
        try:
            while client_id in self.active_connections:
                # Check if client has been inactive for too long
                current_time = time.time()
                last_active = self.last_activity.get(client_id, 0)
                inactive_time = current_time - last_active
                
                if inactive_time > self.heartbeat_timeout:
                    logger.warning(f"Client inactive for too long, disconnecting: client_id={client_id}, inactive_time={inactive_time:.1f}s")
                    await self.disconnect(client_id)
                    break
                
                # Send heartbeat if needed
                if inactive_time > self.heartbeat_interval:
                    logger.debug(f"Client inactive, sending heartbeat: client_id={client_id}, inactive_time={inactive_time:.1f}s")
                    success = await self.heartbeat(client_id)
                    if not success:
                        logger.warning(f"Heartbeat failed, disconnecting client: client_id={client_id}")
                        await self.disconnect(client_id)
                        break
                
                # Wait before next check
                await asyncio.sleep(min(5, self.heartbeat_interval / 2))
                
        except asyncio.CancelledError:
            logger.debug(f"Heartbeat task cancelled: client_id={client_id}")
            raise
        except Exception as e:
            logger.error(f"Error in heartbeat loop: client_id={client_id}, error={str(e)}")
            await self.disconnect(client_id)
    
    def is_connected(self, client_id: str) -> bool:
        """
        Check if a client is connected
        
        Args:
            client_id: Client ID to check
            
        Returns:
            True if connected, False otherwise
        """
        return client_id in self.active_connections
    
    def get_timestamp(self) -> int:
        """
        Get current timestamp in milliseconds
        
        Returns:
            Current timestamp
        """
        return int(time.time() * 1000)
    
    def get_connections_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all active connections
        
        Returns:
            List of connection information
        """
        connections = []
        current_time = time.time()
        
        for client_id, _ in self.active_connections.items():
            last_active = self.last_activity.get(client_id, 0)
            connections.append({
                "client_id": client_id,
                "connected_at": last_active,
                "idle_time": current_time - last_active
            })
        
        return connections

# Create global connection manager instance
manager = ConnectionManager()