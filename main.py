from fastapi import FastAPI
from AT import sms, ussd

app = FastAPI(title='MedNet')

app.include_router(sms.router)
app.include_router(ussd.router)


@app.get("/")
async def healthh_check():
    return("hello")



@app.post("/facilities-me")
async def facilities_code():
    pass



