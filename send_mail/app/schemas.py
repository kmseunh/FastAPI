from pydantic import BaseModel


class EmailSchema(BaseModel):
    recipients: list
    subject: str
    body: str
