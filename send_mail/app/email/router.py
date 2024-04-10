from fastapi import APIRouter, HTTPException

from app.email.service import send_email
from app.schemas import EmailSchema

router = APIRouter()


@router.post("/send-email/")
async def send_email_route(email: EmailSchema):
    try:
        email_data = email.dict()
        await send_email(email_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": "Email sent successfully"}
