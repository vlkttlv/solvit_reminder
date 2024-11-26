from fastapi import APIRouter, Query, BackgroundTasks
from app.questions.dao import QuestionsDAO
from app.questions.services import get_data
from app.tasks.tasks import periodic_send_email
from typing import List
router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"]
)

base_url = "https://solvit.space/questions/"
all_topics = ["Python", "Базы данных и SQL", "Git", "Docker",
              "Вопросы от рекрутеров", "Java", "C#", "C++", "Golang",
              "JavaScript", "HTML", "CSS", "Computer Science"]
all_grades = ["Стажёр", "Джун", "Мидл", "Сеньор"]


@router.post("/add")
async def add_questions_in_db(
    grades: List[str] = Query(default=all_grades),
    topics: List[str] = Query(default=all_topics)):
    """Эндпоинт добавляет вопросы в базу данных на основе указанных грейдов и технологий."""
    count = 0
    for i in range(2500, 2745):
        url = f"{base_url}{i}"  # URL для получения вопроса по номеру
        data = get_data(url, topics, grades)
        if data is not None:
            print(
                f"Была добавлена запись: {
                  data['technology']} - {data['grade']} - {url}"
            )
            count += 1
            await QuestionsDAO.add(**data)
    return {"status": "success",
            "details": f"Было добавлено {count} вопросов"}


@router.get("/get")
async def get_questions(
    background_tasks: BackgroundTasks,
    grades: List[str] = Query(default=all_grades),
    topics: List[str] = Query(default=all_topics),
    period_time: int = Query(default=180, description="Периодичность указывается в минутах"),
    email: str = "email@gmail.com",):
    """
    Эндпоинт получает список вопросов и настраивает периодическую \
    отправку электронных писем с указанным содержимым.
    """
    all_questions = await QuestionsDAO.find_all(topics, grades)
    background_tasks.add_task(periodic_send_email, email, period_time, all_questions)
    return {"status": "success",
            "message": f"Письма будут отправляться каждые {period_time} минут. \
                        Всего вопросов: {len(all_questions)}"}



@router.get("/get_questions")
async def get_all_questions(grades: List[str] = Query(default=all_grades),
                            topics: List[str] = Query(default=all_topics)):
    all_questions = await QuestionsDAO.find_all(topics, grades)
    return all_questions

