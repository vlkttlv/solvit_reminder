from sqlalchemy import select, insert, and_
from app.questions.models import Questions
from app.database import async_session_maker


class QuestionsDAO():
    """Класс для работы с БД"""

    model = Questions

    @classmethod
    async def find_all_by_topics_grades(cls, topics, grades):
        '''
        Находит и возвращает все записи из БД, удовлетворяющие условию,
        что грейд и технология есть в списке, который передал пользователь
        '''
        async with async_session_maker() as session:
            query = select(cls.model).where(
                and_(cls.model.technology.in_(topics), cls.model.grade.in_(grades)))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        '''
        Добавляет запись в БД
        '''
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            res = await session.execute(query)
            await session.commit()  # фиксирует изменения в БД, обязательно
            new_id = res.scalar()  # Получаем id новой записи
            return new_id
