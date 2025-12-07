# app/api/api_v1/messaging.py
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db, require_roles
from app.schemas import MessageCreate, MessageOut, ConversationOut
from app.services.messaging_service import MessagingService
from app.repos.messaging_repo import MessagingRepo

router = APIRouter(prefix="/api/v1", tags=["messaging"])

# Conversations
@router.post("/conversations", response_model=ConversationOut, status_code=status.HTTP_201_CREATED)
def create_conversation(title: Optional[str] = None, db: Session = Depends(get_db),
                        current_user = Depends(require_roles("admin", "manager", "staff"))):
    svc = MessagingService(db, MessagingRepo)
    conv = svc.start_conversation(title)
    return conv

@router.get("/conversations", response_model=List[ConversationOut])
def list_conversations(db: Session = Depends(get_db),
                       current_user = Depends(require_roles("admin", "manager", "staff"))):
    svc = MessagingService(db, MessagingRepo)
    return svc.repo.list_conversations()

@router.get("/conversations/{conv_id}", response_model=ConversationOut)
def get_conversation(conv_id: int, db: Session = Depends(get_db),
                     current_user = Depends(require_roles("admin", "manager", "staff"))):
    svc = MessagingService(db, MessagingRepo)
    conv = svc.repo.get_conversation(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

# Messages (nested resource)
@router.post("/conversations/{conv_id}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def post_message(conv_id: int, payload: MessageCreate, db: Session = Depends(get_db),
                 current_user = Depends(require_roles("admin","manager","staff"))):
    # Basic protection: ensure conv_id matches payload (if provided)
    if payload.conversation_id != conv_id:
        raise HTTPException(status_code=400, detail="conversation_id mismatch")
    svc = MessagingService(db, MessagingRepo)
    try:
        msg = svc.send_message(conv_id, payload.sender_id, payload.content)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return msg

@router.get("/conversations/{conv_id}/messages", response_model=List[MessageOut])
def get_messages(conv_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db),
                 current_user = Depends(require_roles("admin","manager","staff"))):
    svc = MessagingService(db, MessagingRepo)
    return svc.fetch_messages(conv_id, limit, offset)

@router.patch("/messages/{message_id}/read", response_model=MessageOut)
def mark_read(message_id: int, db: Session = Depends(get_db),
              current_user = Depends(require_roles("admin","manager","staff"))):
    svc = MessagingService(db, MessagingRepo)
    m = svc.mark_as_read(message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return m

# Minimal WebSocket endpoint for real-time (simple)
@router.websocket("/api/v1/ws/conversations/{conv_id}")
async def ws_conversation(websocket: WebSocket, conv_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # data expected: {"sender_id": int, "content": str}
            # Echo back - production: save to DB and broadcast to others
            await websocket.send_json({
                "conversation_id": conv_id,
                "sender_id": data.get("sender_id"),
                "content": data.get("content"),
                "received_at": None
            })
    except WebSocketDisconnect:
        pass
