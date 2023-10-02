import requests
import os
from Mountain_pass import settings


file_path = os.path.join(settings.BASE_DIR, 'images', "image0000001.png")

data = {
    "country": "РФ",
    "category": "гора",
    "title": "Егоза",
    "other_titles": "",
    "add_time": "2023-08-10 12:00:00",
    "status": "new",
    "user": {
        "surname": "Голубева",
        "name": "Елена",
        "patronymic": "Васильевна",
        "email": "kir2845@mail.ru",
        "telephone": "+79518001704"
    },
    "coords": {
        "latitude": "45.3842",
        "longitude": "7.1525",
        "height": "1200"
    },
    "level": {
        "winter": "2A",
        "spring": "1A",
        "summer": "1A",
        "autumn": "1A"
    },
 #   "images": {
  #      "title": "45.3842",
  #      "photo": "7.1525",
  #  },
}

url = 'http://127.0.0.1:8000/Mountain_pass/submit_data/'

# Преобразование данных для изображений в кортежи
image_files = [('images', ('image0000001.png', open(file_path, 'rb'), 'image/png'))]

# Отправка POST запроса с данными в виде словаря и файлами для изображений
response = requests.post(url, data=data, files=image_files)
print(response.status_code)
print(response.text)

