import requests
import json

def get_prediction(cards, question):
    try:
        
        cards_description = "\n".join(
            [f"{i+1}. {card['name']} ({'Перевернутая' if card['position'] == 'reversed' else 'Прямая'})" 
             for i, card in enumerate(cards)]
        )

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
            },
             data=json.dumps({
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": """Ты опытный таролог с 20-летним стажем. Пиши толкования как живой человек:
                        1. Избегай шаблонных фраз вроде "эта карта означает"
                        2. Пиши единым текстом без нумерованных списков
                        3. Используй естественные паузы и разговорные конструкции
                        4. Допускай небольшую непоследовательность мыслей
                        5. Вплетай вопрос клиента в толкование
                        6. Избегай излишней формальности
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""Вот что выпало клиенту: {cards_description}. 
                        Он спрашивает вот о чем: "{question}".
                        
                        Напиши развернутое толкование как профессиональный таролог - 
                        единым связным текстом, будто объясняешь человеку за столом. 
                        Пусть будет немного ассоциаций и личных наблюдений, 
                        как в реальной консультации."""
                    }
                ],
                "temperature": 0.7  
            }),
            timeout=15
        )

        if response.status_code != 200:
            return f"Ошибка API (код {response.status_code})"

        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "Не удалось получить предсказание")

    except requests.exceptions.RequestException as e:
        return f"Ошибка соединения: {str(e)}"
    except Exception as e:
        return f"Ошибка обработки ответа: {str(e)}"
    
    