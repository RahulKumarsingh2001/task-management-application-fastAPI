from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

    
    
conf = ConnectionConfig(
    MAIL_USERNAME = "rahulsingh68644@gmail.com",
    MAIL_PASSWORD = "afal kquh nbzb jaxf",
    MAIL_FROM = "rahulsingh68644@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)    




async def send_email(emails: List[str]):
    html = """<p>Hi, thankyou for registation. </br> Your team will connect you soon.</p> """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}