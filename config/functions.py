from pprint import pprint
from typing import Annotated
from db.database import get_session
from AT.sms_config import SMS
from sqlmodel import select, Session
from fastapi import Depends
from db.models import Facility, MedicineInventory, SharingRequest



def create_facility(db, name: str, location: str, contact_info: str, license_number: str, type: str):
    if type.lower() not in ["clinic", "pharmacy"]:
        SMS().send("Invalid facility type. Please use 'clinic' or 'pharmacy'.")
    
    new_facility = Facility(
        name=name.title(),
        type=type.lower(),
        license_number=license_number,
        location=location,
        contact_info=contact_info
    )
        
    db.add(new_facility)
    db.commit()
    db.refresh(new_facility)

    # creates the facility code 
    new_facility.facility_code = f"{new_facility.type[:5].upper()}-{new_facility.id}"
    db.add(new_facility)
    db.commit()
    db.refresh(new_facility)
    
    return {"name": new_facility.name, "facility_code": new_facility.facility_code}

def create_medicine_inventory(db, facility_code: str, medicine_name: str, quantity: str, expiry_date: str):
    # Check if facility exists
    statement = select(Facility).where(Facility.facility_code == facility_code)
    facility = db.exec(statement).first()
    if not facility:
        return False
    
    # Create new medicine inventory
    new_inventory = MedicineInventory(
        facility_code=facility_code,
        medicine_name=medicine_name.title(),
        quantity=int(quantity),
        expiry_date=expiry_date
    )
    
    # Add to database
    db.add(new_inventory)
    db.commit()
    
    return {
        "facility_code": new_inventory.facility_code,
        "medicine_name": new_inventory.medicine_name,
        "quantity": new_inventory.quantity,
    }

def search_medicines(db, location: str = None, medicine_name: str = None):
    """
    Filter medicines by location and medicine name
    """
    
    # Start with base query joining MedicineInventory and Facility
    statement = select(MedicineInventory, Facility).join(
        Facility, MedicineInventory.facility_code == Facility.facility_code
    )
    
    # Apply filters if provided
    if location:
        statement = statement.where(Facility.location.ilike(f"%{location}%"))
    
    if medicine_name:
        statement = statement.where(MedicineInventory.medicine_name.ilike(f"%{medicine_name}%"))
    
    # Execute query
    results = db.exec(statement).all()
    
    if not results:   
        return None
    # Format results 
    message = f"Found {medicine_name} in {location}:\n"
    for med, facility in results[:3]:
        message += f"- {facility.name} (Contact: {facility.contact_info})\n"

    return message