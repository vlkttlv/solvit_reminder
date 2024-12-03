import asyncio
import smtplib
import ssl
from pydantic import EmailStr, parse_obj_as
from app.config import settings
from app.questions.schemas import SQuestion
from app.tasks.email_template import create_message_template


async def send_question_email(
    question: dict,
    email_to: EmailStr,
):
    """Отправляет электронное письмо с содержимым вопроса указанному адресату.

    Эта функция создает сообщение с помощью шаблона и отправляет его через SMTP-сервер"""

    msg_content = create_message_template(question, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)

    print(f"Письмо было успешно отправлено по адресу {email_to}")


async def periodic_send_email(email_to: EmailStr, period_time: int, questions: list):
    """Периодически отправляет вопросы на указанный адрес электронной почты.

    Эта функция отправляет каждый вопрос из переданного списка 
    на указанный адрес электронной почты с указанным интервалом 
    (в минутах) между отправками."""

    for question in questions:
        question_dict = parse_obj_as(SQuestion, question).dict()
        await send_question_email(question_dict, email_to)
        await asyncio.sleep(period_time * 60)
