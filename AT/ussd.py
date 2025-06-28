from fastapi import APIRouter, Request

router = APIRouter(prefix="/ussd", tags=["ussd"])

@router.post("/")
async def facility_ussd(request: Request):
    # Read the variables sent via POST from our API
    # session_id   = request.values.get("sessionId", None)
    # serviceCode  = request.values.get("serviceCode", None)
    # phone_number = request.values.get("phoneNumber", None)
    # text         = request.values.get("text", "default")
    text = ""
    phone_number = "08106422202"
    form = await request.form()
    print("📨 Incoming SMS Payload:")
    print(dict(form))

    if text == '':
        # This is the first request. Note how we start the response with CON
        response  = "CON What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"
    elif text == '1':
        # Business logic for first level response
        response = "CON Choose account information you want to view \n"
        response += "1. Account number"
    elif text == '2':
        # This is a terminal request. Note how we start the response with END
        response = "END Your phone number is " + phone_number
    elif text == '1*1':
        # This is a second level response where the user selected 1 in the first instance
        accountNumber  = "ACC1001"
        # This is a terminal request. Note how we start the response with END
        response = "END Your account number is " + accountNumber
    else :
        response = "END Invalid choice"
    # Send the response back to the API
    return response