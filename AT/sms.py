from AT.sms_config import SMS
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/sms", tags=["sms"])


@router.post("/find-medicine/", response_class=PlainTextResponse)
async def find_medicine(request: Request):
    form = await request.form()
    print("📨 Incoming SMS Payload:")
    # gets the payll
    payload = dict(form)
    print(payload)
    text = payload.get("text", "")

    #checks if the text contains "FIND"
    if "FIND" not in text:
        SMS().send("Wrong Code")
        
    else:
        drug = text.split(" ")[1]
        SMS().send(f"{drug.title()} Found")
