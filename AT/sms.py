from typing import Annotated
from sqlmodel import Session
from db.database import get_session
from AT.sms_config import SMS
from config.functions import *
from fastapi import APIRouter, Request, Depends


router = APIRouter(prefix="/sms", tags=["sms"])

db_dependency = Annotated[Session, Depends(get_session)]


@router.post("/")
async def sms_callback_url(request: Request, db: db_dependency) -> None:
    form = await request.form()
    print("📨 Incoming SMS Payload:")

    # gets the payload
    payload = dict(form)
    print(payload)

    # gets the text written by the user sent to our shortcode
    text = payload.get("text", "")
    text_data = text.split(" ")
    code = text_data[0].upper()  # Get the first word and convert to uppercase
    print(text_data)

    #checks if the text contains "FIND"
    if "FIND" == code:
        # This is how the data would be sent by the user
        # FIND [medicine_name] [location]

        available_medicines = search_medicines(
            db=db, 
            medicine_name=text_data[1], 
            location=text_data[2]
        )
        
        # Format the results for SMS
        if meds := available_medicines:
            SMS().send(meds)
        else:
            SMS().send(f"No {text_data[1]} found in {text_data[2]}")

    
    elif "REGISTER" == code:
        # This is how the data would be sent by the user
        # REGISTER [name] [location] [contact_info] [license_number] [type]

        # create a new facility in the DB 
        facility_details = create_facility(
            db=db, 
            name=text_data[1], 
            location=text_data[2], 
            contact_info=text_data[3],
            license_number=text_data[4],
            type=text_data[5]
            )
        SMS().send(f"Welcome {facility_details.get('name')}.\nYour Facility Code is {facility_details.get('facility_code')}")


    elif "STOCK" == code:
        # This is how the data would be sent by the user
        # STOCK [facility_code] [medicine_name] [quantity] [expiry_date]
        new_med = create_medicine_inventory(
            db=db, 
            facility_code=text_data[1], 
            medicine_name=text_data[2], 
            quantity=text_data[3], 
            expiry_date=text_data[4]
            )
        
        if not new_med:
            SMS().send(f"Facility with (facility code: {text_data[1]}) not found")
            print("facility no found")
        else: 
            SMS().send(f"{new_med.get('quantity')} amount of {new_med.get('medicine_name')} \
                       has been added to {new_med.get('facility_code')} inventory")
            print("facility found")
        
    else:
        SMS().send("Wrong Code")


