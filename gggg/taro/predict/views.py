from django.shortcuts import render, redirect
import random
from django.views.decorators.csrf import csrf_protect
from .models import TarotCard, Reading, DrawnCard
from .taro_ai import get_prediction
from django.utils import timezone
from django.http import HttpResponseRedirect
# views.py
import os
from django.conf import settings
from django.shortcuts import render

def tarot_view(request):
    cards_dir = os.path.join(settings.BASE_DIR, 'taro', 'media', 'tarot_cards')
    card_files = [f for f in os.listdir(cards_dir) if f.endswith('.png')]
    card_urls = [os.path.join(settings.MEDIA_URL, 'tarot_cards', f) for f in card_files]
    
    return render(request, 'tarot.html', {'tarot_cards': card_urls})

@csrf_protect
def taro_view(request):
    # Обработка карты дня
    if request.method == 'POST' and 'card_of_day' in request.POST:
        all_cards = TarotCard.objects.all()
        if not all_cards.exists():
            return render(request, 'home.html', {
                'error': 'В базе данных нет карт. Добавьте карты через админку.'
            })
        
        today = timezone.now().date()
        random.seed(today.toordinal())
        card = random.choice(list(all_cards))
        is_reversed = random.choice([True, False])
        
        cards_for_api = [{
            'name': card.name,
            'position': 'reversed' if is_reversed else 'upright'
        }]
        
        try:
            prediction = get_prediction(cards_for_api, "Какая энергия и совет для меня сегодня?")
            if prediction.startswith("Ошибка"):
                return render(request, 'home.html', {
                    'error': prediction
                })
            
            advice_response = get_prediction(cards_for_api, "Сформулируй краткий практический совет на основе этой карты")
            
            return render(request, 'home.html', {
                'card_of_day': {
                    'card': card,
                    'reversed': is_reversed
                },
                'card_of_day_prediction': prediction,
                'card_of_day_advice': advice_response if not advice_response.startswith("Ошибка") else None
            })
        except Exception as e:
            return render(request, 'home.html', {
                'error': f'Системная ошибка при получении карты дня: {str(e)}'
            })
    
    # Обработка основного расклада
    elif request.method == 'POST' and 'question' in request.POST:
        question = request.POST.get('question', '').strip()
        if question:
            try:
                cards_number = min(max(int(request.POST.get('cards-number', 3)), 1), 5)
            except ValueError:
                cards_number = 3
            
            all_cards = TarotCard.objects.all()
            if not all_cards.exists():
                return render(request, 'home.html', {
                    'error': 'В базе данных нет карт. Добавьте карты через админку.'
                })
            
            # Сбрасываем seed для случайного выбора карт
            random.seed()
            selected_cards = random.sample(list(all_cards), min(cards_number, all_cards.count()))
            
            reading = Reading.objects.create(question=question)
            
            cards_for_display = []
            cards_for_api = []
            
            for card in selected_cards:
                is_reversed = random.choice([True, False])
                
                DrawnCard.objects.create(
                    reading=reading,
                    card=card,
                    reversed=is_reversed
                )
                
                cards_for_display.append({
                    'card': card,
                    'reversed': is_reversed
                })
                
                cards_for_api.append({
                    'name': card.name,
                    'position': 'reversed' if is_reversed else 'upright'
                })
            
            try:
                prediction = get_prediction(cards_for_api, question)
                if prediction.startswith("Ошибка"):
                    return render(request, 'home.html', {
                        'error': prediction,
                        'question': question,
                        'cards': cards_for_display
                    })
                reading.prediction = prediction
                reading.save()
            except Exception as e:
                return render(request, 'home.html', {
                    'error': f'Системная ошибка при толковании расклада: {str(e)}',
                    'question': question,
                    'cards': cards_for_display
                })
            
            return render(request, 'home.html', {
                'question': question,
                'cards': cards_for_display,
                'prediction': prediction
            })
    
    return render(request, 'home.html')