from app.models import AuditLog, ActivityFeed

class AuditRepo:
    def __init__(self, db): self.db = db
    def add_log(self, log: AuditLog):
        self.db.add(log); self.db.commit(); self.db.refresh(log); return log
    def list_logs(self, entity=None, limit=50):
        q = self.db.query(AuditLog)
        if entity:
            q = q.filter(AuditLog.entity == entity)
        return q.order_by(AuditLog.created_at.desc()).limit(limit).all()

class ActivityRepo:
    def __init__(self, db): self.db = db
    def add(self, activity: ActivityFeed):
        self.db.add(activity); self.db.commit(); self.db.refresh(activity); return activity
    def recent_for_user(self, user_id, limit=20):
        return (self.db.query(ActivityFeed)
                .filter(ActivityFeed.user_id == user_id)
                .order_by(ActivityFeed.created_at.desc())
                .limit(limit).all())
