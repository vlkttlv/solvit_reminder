import requests
from bs4 import BeautifulSoup
from app.questions.dao import QuestionsDAO

base_url = "https://solvit.space/questions/"

def get_data(url, topics, grades):
    response = requests.get(url) 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all("script") 
        soup_title = soup.title 
        title = soup_title.string
        current_topic = ''
        current_grade = ''
        for topic in topics:
            if topic in title:
                current_topic = topic
        if current_topic == '':
            return None
        if 'Стажёр' in soup.text :
            current_grade = 'Стажёр'
        else:
            for grade in grades:
                for script in scripts:
                    if grade in script.text:
                        current_grade = grade
        print(f"{current_topic} - {current_grade} - {url}")
        return {"url": url, "technology": current_topic, "grade": current_grade}


async def add_questions_in_db():
    for i in range(0, 3000):
        url = f"{base_url}{i}"  # URL для получения вопроса по номеру
        data = get_data(url)
        if data != None:
            await QuestionsDAO.add(**data)
