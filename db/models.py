from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# ---------- Facility ----------
class Facility(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: str = Field(index=True, unique=True)
    location: str
    contact_info: str

    # Relationships
    inventory: list["MedicineInventory"] = Relationship(back_populates="facility")
    sent_requests: list["SharingRequest"] = Relationship(back_populates="from_facility", sa_relationship_kwargs={"foreign_keys": "[SharingRequest.from_facility_id]"})
    received_requests: list["SharingRequest"] = Relationship(back_populates="to_facility", sa_relationship_kwargs={"foreign_keys": "[SharingRequest.to_facility_id]"})


# ---------- Medicine Inventory ----------
class MedicineInventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    facility_id: int = Field(foreign_key="facility.id")
    medicine_name: str
    quantity: int
    expiry_date: datetime
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    facility: Facility = Relationship(back_populates="inventory")


# ---------- Sharing Request ----------
class SharingRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_facility_id: int = Field(foreign_key="facility.id")
    to_facility_id: int = Field(foreign_key="facility.id")
    medicine_name: str
    quantity: int
    status: str = Field(default="pending")  # pending, accepted, rejected
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    from_facility: Facility = Relationship(back_populates="sent_requests", sa_relationship_kwargs={"foreign_keys": "[SharingRequest.from_facility_id]"})
    to_facility: Facility = Relationship(back_populates="received_requests", sa_relationship_kwargs={"foreign_keys": "[SharingRequest.to_facility_id]"})
