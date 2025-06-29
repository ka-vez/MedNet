from db.database import init_db
from fastapi import FastAPI
from AT import sms, ussd
from db.models import Facility, MedicineInventory, SharingRequest


init_db()  # Initialize the database
app = FastAPI(title='MedNet')

app.include_router(sms.router)
app.include_router(ussd.router)