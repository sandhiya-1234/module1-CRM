class MessagingService:
    def __init__(self, db, repo_cls):
        self.db = db
        self.repo = repo_cls(db)

    def start_conversation(self, title=None):
        return self.repo.create_conversation(title)

    def send_message(self, conversation_id, sender_id, content):
        # validate conversation exists
        conv = self.repo.get_conversation(conversation_id)
        if not conv:
            raise ValueError("Conversation not found")
        return self.repo.add_message(conversation_id, sender_id, content)

    def fetch_messages(self, conversation_id, limit=100, offset=0):
        return self.repo.list_messages(conversation_id, limit, offset)

    def mark_as_read(self, message_id):
        return self.repo.mark_read(message_id)
