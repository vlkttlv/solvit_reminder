from bs4 import BeautifulSoup
import requests


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
        if 'Стажёр' in soup.text and 'Стажёр' in grades:
            current_grade = 'Стажёр'
        else:
            for grade in grades:
                for script in scripts:
                    if grade in script.text:
                        current_grade = grade

        return {"url": url, "technology": current_topic, "grade": current_grade}
