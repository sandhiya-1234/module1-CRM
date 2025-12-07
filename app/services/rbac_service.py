from fastapi import HTTPException, status

class RBACService:
    def __init__(self, db, role_repo):
        self.db = db
        self.role_repo = role_repo

    def has_role(self, user_id, required_roles: list[str]):
        roles = self.role_repo(self.db).roles_for_user(user_id)
        names = {r.name for r in roles}
        return any(role in names for role in required_roles)

    def enforce(self, user_id, required_roles):
        if not self.has_role(user_id, required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges"
            )
