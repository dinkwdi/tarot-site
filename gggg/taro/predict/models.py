from django.db import models

class TarotCard(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название карты")
    image = models.ImageField(upload_to='tarot_cards/', verbose_name="Изображение карты")
    
    class Meta:
        verbose_name = "Карта Таро"
        verbose_name_plural = "Карты Таро"

    def __str__(self):
        return self.name

class Reading(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    prediction = models.TextField(verbose_name="Предсказание")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Расклад"
        verbose_name_plural = "Расклады"

class DrawnCard(models.Model):
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE, related_name='drawn_cards')
    card = models.ForeignKey(TarotCard, on_delete=models.CASCADE)
    reversed = models.BooleanField(default=False, verbose_name="Перевернутая")
    
    class Meta:
        verbose_name = "Выпавшая карта"
        verbose_name_plural = "Выпавшие карты"