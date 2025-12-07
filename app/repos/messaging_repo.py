from mailbox import Message
from app.models import Conversation


class MessagingRepo:
    def __init__(self, db):
        self.db = db

    def create_conversation(self, title=None):
        conv = Conversation(title=title)
        self.db.add(conv); self.db.commit(); self.db.refresh(conv)
        return conv

    def get_conversation(self, conv_id):
        return self.db.query(Conversation).get(conv_id)

    def list_conversations(self):
        return self.db.query(Conversation).order_by(Conversation.created_at.desc()).all()

    def add_message(self, conversation_id, sender_id, content):
        msg = Message(conversation_id=conversation_id, sender_id=sender_id, content=content)
        self.db.add(msg); self.db.commit(); self.db.refresh(msg)
        return msg

    def list_messages(self, conversation_id, limit=100, offset=0):
        return (self.db.query(Message)
                    .filter(Message.conversation_id == conversation_id)
                    .order_by(Message.created_at.asc())
                    .limit(limit).offset(offset).all())

    def mark_read(self, message_id):
        m = self.db.query(Message).get(message_id)
        if m:
            m.is_read = True; self.db.commit(); self.db.refresh(m)
        return m
