from django.test import TestCase
from .models import TarotCard, Reading, DrawnCard
from django.core.files.uploadedfile import SimpleUploadedFile

class TarotCardModelTest(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.card = TarotCard.objects.create(name="Шут", image=image)

    def test_tarot_card_creation(self):
        self.assertEqual(self.card.name, "Шут")
        self.assertTrue(self.card.image.name.startswith('tarot_cards/'))
    
    def test_str_method(self):
        self.assertEqual(str(self.card), "Шут")

class ReadingModelTest(TestCase):
    def setUp(self):
        self.reading = Reading.objects.create(question="Что меня ждёт?", prediction="Удача и успех")

    def test_reading_creation(self):
        self.assertEqual(self.reading.question, "Что меня ждёт?")
        self.assertEqual(self.reading.prediction, "Удача и успех")
        self.assertIsNotNone(self.reading.created_at)

class DrawnCardModelTest(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.card = TarotCard.objects.create(name="Маг", image=image)
        self.reading = Reading.objects.create(question="Как сложится день?", prediction="Будет продуктивным")
        self.drawn_card = DrawnCard.objects.create(reading=self.reading, card=self.card, reversed=True)

    def test_drawn_card_creation(self):
        self.assertEqual(self.drawn_card.reading, self.reading)
        self.assertEqual(self.drawn_card.card, self.card)
        self.assertTrue(self.drawn_card.reversed)
