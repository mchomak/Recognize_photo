from openai import OpenAI
import requests
import os
from config import Config


api_key = Config["api_key"]


os.environ['HTTP_PROXY'] = Config["proxy1"]
os.environ['HTTPS_PROXY'] = Config["proxy2"]


client = OpenAI(api_key=api_key)


def processing_data(data):
    syn = []
    for i in data:
        if len(i) > 2 and "English" not in i:
            if " " in i:
                for s in i.split(" "):
                    if len(s) > 2:
                        syn.append(s)
            else:
                syn.append(i)
    return syn



def get_synonyms(word, examples):
    completion = client.chat.completions.create(
    model="gpt-4o",
    max_tokens= 100,
    messages = [
        {
            "role": "system", 
            "content": "You're an assistant for finding synonyms for the word."
        },
        {
            "role": "user", 
            "content": 
            [
                {
                "type": "text",
                "text": 
                f"""
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
    mes = completion.choices[0].message.content.split("Russian")

    eng = mes[0].split("\n")
    rus = mes[1].split("\n")
 
    return processing_data(eng) + processing_data(rus)


print(get_synonyms("машина", 5))