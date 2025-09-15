# app/services/lead_service.py
from sqlalchemy.exc import SQLAlchemyError

class LeadService:
    def __init__(self, lead_repo_class, deal_repo_class, db_session):
        self.lead_repo_class = lead_repo_class
        self.deal_repo_class = deal_repo_class
        self.db = db_session

    def create_lead(self, name: str, email: str = None):
        repo = self.lead_repo_class(self.db)
        return repo.create(name=name, email=email)

    def promote_to_deal(self, lead_id: int, value_cents: int, seller_id: int = None):
        try:
            with self.db.begin():
                lead_repo = self.lead_repo_class(self.db)
                deal_repo = self.deal_repo_class(self.db)

                lead = lead_repo.get(lead_id)
                if not lead:
                    raise ValueError("Lead not found")

                if lead.status == "converted":
                    raise ValueError("Lead already converted")

                deal = deal_repo.create(lead_id=lead.id, value_cents=value_cents, seller_id=seller_id)
                lead.status = "converted"
                self.db.add(lead)
            return deal
        except SQLAlchemyError:
            self.db.rollback()
            raise
