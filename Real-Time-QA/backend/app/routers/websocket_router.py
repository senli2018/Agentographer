"""
WebSocket Chat Routes
"""
import uuid
import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from app.services.websocket_service import manager
from app.utils.logger import logger
from app.core.config import settings
from typing import List, Dict, Any

router = APIRouter(tags=["WebSocket Chat"])

@router.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """
    WebSocket chat endpoint (with client ID)
    
    Args:
        websocket: WebSocket connection
        client_id: Client ID
    """
    connection_accepted = False
    
    try:
        # Accept connection first, ensure WebSocket is established
        logger.info(f"Accepting WebSocket connection: client_id={client_id}")
        
        # Set connection timeout
        try:
            # Use timeout mechanism to accept connection
            await asyncio.wait_for(
                websocket.accept(),
                timeout=settings.WEBSOCKET_CONNECTION_TIMEOUT
            )
            connection_accepted = True
            logger.info(f"WebSocket connection accepted: client_id={client_id}")
        except asyncio.TimeoutError:
            logger.error(f"WebSocket connection accept timeout: client_id={client_id}")
            return  # Return directly, no further processing
        
        # Then register to connection manager
        try:
            await manager.connect(websocket, client_id)
        except RuntimeError as e:
            if "WebSocket is not connected" in str(e):
                logger.error(f"Failed to register WebSocket: client_id={client_id}, error={str(e)}")
                return
            raise
        
        # Send welcome message
        welcome_message = {
            "type": "system",
            "content": "Connected to chat server. Start chatting!",
            "timestamp": manager.get_timestamp(),
            "client_id": client_id
        }
        await manager.send_personal_message(welcome_message, client_id)
        
        # Start heartbeat task
        heartbeat_task = asyncio.create_task(
            manager.heartbeat(client_id)
        )
        
        try:
            # Main message processing loop
            while True:
                # Wait for message with timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_text(),
                        timeout=settings.WEBSOCKET_RECEIVE_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    # No message received within timeout, check if client is still connected
                    if not manager.is_connected(client_id):
                        logger.info(f"Client disconnected during receive timeout: client_id={client_id}")
                        break
                    # Client still connected, continue waiting
                    continue
                
                # Process received message
                try:
                    message_data = json.loads(data)
                    
                    # Handle different message types
                    message_type = message_data.get("type", "chat")
                    
                    if message_type == "ping":
                        # Ping message for keeping connection alive
                        await manager.send_personal_message(
                            {"type": "pong", "timestamp": manager.get_timestamp()},
                            client_id
                        )
                    elif message_type == "chat":
                        # Regular chat message
                        content = message_data.get("content", "").strip()
                        if not content:
                            continue
                        
                        # Process chat message
                        await manager.process_chat_message(client_id, content)
                    else:
                        # Unknown message type
                        logger.warning(f"Unknown message type: {message_type}, client_id={client_id}")
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from client: client_id={client_id}")
                    await manager.send_personal_message(
                        {"type": "error", "content": "Invalid message format. Please send valid JSON."},
                        client_id
                    )
                except Exception as e:
                    logger.error(f"Error processing message: client_id={client_id}, error={str(e)}")
                    await manager.send_personal_message(
                        {"type": "error", "content": f"Error processing message: {str(e)}"},
                        client_id
                    )
        finally:
            # Cancel heartbeat task when exiting the loop
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: client_id={client_id}")
    except Exception as e:
        logger.error(f"WebSocket error: client_id={client_id}, error={str(e)}")
    finally:
        # Clean up connection if it was accepted
        if connection_accepted:
            await manager.disconnect(client_id)
            logger.info(f"Client disconnected and removed from manager: client_id={client_id}")

@router.websocket("/ws/chat")
async def websocket_chat_auto_id(websocket: WebSocket):
    """
    WebSocket chat endpoint (auto-generated client ID)
    
    This endpoint automatically generates a client ID and then delegates to the main
    websocket_chat endpoint.
    
    Args:
        websocket: WebSocket connection
    """
    # Generate a unique client ID
    client_id = str(uuid.uuid4())
    logger.info(f"Auto-generated client ID for WebSocket connection: client_id={client_id}")
    
    # Delegate to the main websocket handler
    await websocket_chat(websocket, client_id)

@router.post("/api/ws/disconnect/{client_id}", status_code=200)
async def disconnect_client(client_id: str):
    """
    Disconnect a client by ID
    
    This API allows administrative disconnection of a client.
    
    Args:
        client_id: Client ID to disconnect
        
    Returns:
        Success message
    """
    if not manager.is_connected(client_id):
        raise HTTPException(status_code=404, detail=f"Client {client_id} not connected")
    
    # Send disconnect message to client
    try:
        await manager.send_personal_message(
            {"type": "system", "content": "You have been disconnected by the server."},
            client_id
        )
    except Exception as e:
        logger.error(f"Error sending disconnect message: client_id={client_id}, error={str(e)}")
    
    # Disconnect the client
    await manager.disconnect(client_id)
    logger.info(f"Client disconnected via API: client_id={client_id}")
    
    return {"status": "success", "message": f"Client {client_id} disconnected"}

@router.get("/api/ws/connections", status_code=200)
async def get_connections():
    """
    Get all active WebSocket connections
    
    Returns:
        List of active connections with client IDs and connection times
    """
    connections = manager.get_connections_info()
    return {
        "status": "success",
        "count": len(connections),
        "connections": connections
    } 