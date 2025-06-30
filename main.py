from db.database import init_db
from fastapi import FastAPI
from AT import sms, ussd
from db.models import Facility, MedicineInventory, SharingRequest


init_db()  # Initialize the database
app = FastAPI(title='MedNet')

app.include_router(sms.router)
app.include_router(ussd.router)

# TODO configure sending sms to be sent to the number the request is coming from

# TODO work on the expiry date notification function

# TODO work on customers setting ALERTS

# TODO work on facilities sending emergency requests to other facilities

# TODO work on AI features to suggest medicines based on symptoms and give clinic closest to the user