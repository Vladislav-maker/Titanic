# Для написания api
from fastapi import FastAPI, Request, HTTPException 

# Для того чтобы поднять веб сервис
import uvicorn

# Для того чтобы поделить правила взаимодействия
from pydantic import BaseModel

import pandas as pd
import pickle

'''
Давайте создадим простое API с тремя ручками: одна для предсказания выживания (/predict), 
другая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
Убедитесь, что у вас установлены необходимые библиотеки:
pip install fastapi uvicorn pydantic scikit-learn pandas

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение: python app_api.py
Шаг 4: Тестирование API
Теперь вы можете протестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP-запросов.

Проверка работы API (/health) через терминал
http://127.0.0.1:5000/docs - просмотр всего что сделано с возможностью теста
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"Pclass\": 3, \"Age\": 22.0, \"Fare\": 7.2500}"
'''

app = FastAPI()

# Загрузка модели из файла pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    Pclass: int
    Age: float
    Fare: float

# стучимся в дверь чтобы что-то получить
@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}


# Передаем данные 
@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    # Создание DataFrame из данных
    new_data = pd.DataFrame({
        'Pclass': [input_data.Pclass],
        'Age': [input_data.Age],
        'Fare': [input_data.Fare]
    })

    # Предсказание
    predictions = model.predict(new_data)

    # Преобразование результата в человеко-читаемый формат
    result = "Survived" if predictions[0] == 1 else "Not Survived"

    return {"prediction": result}

if __name__ == '__main__':
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=5000) # localhost
    uvicorn.run(app, host="0.0.0.0", port=5000) # в докере нужно писать так