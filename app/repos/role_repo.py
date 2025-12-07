from app.models import Role, UserRole

class RoleRepo:
    def __init__(self, db):
        self.db = db

    def get_role(self, name):
        return self.db.query(Role).filter(Role.name == name).first()

    def assign_role(self, user_id, role_id):
        ur = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(ur)
        self.db.commit()
        self.db.refresh(ur)
        return ur

    def roles_for_user(self, user_id):
        return (
            self.db.query(Role)
            .join(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )
