from openai import OpenAI  
import requests  
import os  
from config import Config  


# Получаем API ключ из конфигурационного файла
api_key = Config["api_key"]


# Устанавливаем переменные окружения для прокси-серверов
os.environ['HTTP_PROXY'] = Config["proxy1"]
os.environ['HTTPS_PROXY'] = Config["proxy2"]


# Создаем клиента OpenAI с использованием API ключа
client = OpenAI(api_key=api_key)


def processing_data(data):
    """
    Обрабатывает входные данные для извлечения подходящих синонимов.
    
    Args:
    data (list): Список строк, содержащий синонимы.
    
    Returns:
    list: Отфильтрованный список синонимов.
    """
    syn = []
    for i in data:
        # Проверяем длину строки и отсутствие слова "English"
        if len(i) > 2 and "English" not in i:
            # Разбиваем строку по пробелам и добавляем слова длиннее 2 символов
            if " " in i:
                for s in i.split(" "):
                    if len(s) > 2:
                        syn.append(s)
            else:
                syn.append(i)
    return syn


def get_synonyms(word, examples):
    """
    Получает список синонимов для заданного слова на английском и русском языках.
    
    Args:
    word (str): Слово, для которого нужно найти синонимы.
    examples (int): Количество примеров синонимов для каждого языка.
    
    Returns:
    list: Список синонимов на английском и русском языках.
    """
    completion = client.chat.completions.create(
        model="gpt-4o",  # Указываем модель GPT-4
        max_tokens=100,  # Максимальное количество токенов в ответе
        messages=[
            {
                "role": "system",
                "content": "You're an assistant for finding synonyms for the word."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        Give me a list of all synonyms of the word {word} in English and Russian, including slang, at least {examples} for each language.
                        No unnecessary symbols or signs.
                        English:
                        Russian:
                        """
                    },
                ]
            }
        ]
    )
    
    # Разделяем ответ на английские и русские синонимы
    mes = completion.choices[0].message.content.split("Russian")
    
    eng = mes[0].split("\n")
    rus = mes[1].split("\n")
    
    # Возвращаем объединенный список синонимов после обработки данных
    return processing_data(eng) + processing_data(rus)


# Тестируем функцию, выводя синонимы для слова "машина"
print(get_synonyms("машина", 5))
