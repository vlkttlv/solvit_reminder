from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings


def create_message_template(
    question: dict,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Новый вопрос"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Ответьте на новый вопрос</h1>
            Ссылка на вопрос: {question['url']}
            Вопрос по теме: {question['technology']}, грейд: {question['grade']}.
        """,
        subtype="html"
    )
    return email
