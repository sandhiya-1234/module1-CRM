from app.models import AuditLog, ActivityFeed

class AuditService:
    def __init__(self, db, audit_repo, activity_repo):
        self.db, self.audit_repo, self.activity_repo = db, audit_repo, activity_repo

    def log_event(self, actor_id, entity, entity_id, action, changes=None):
        log = AuditLog(actor_id=actor_id, entity=entity, entity_id=entity_id,
                       action=action, changes=changes or {})
        return self.audit_repo(self.db).add_log(log)

    def post_activity(self, user_id, message):
        feed = ActivityFeed(user_id=user_id, message=message)
        return self.activity_repo(self.db).add(feed)
