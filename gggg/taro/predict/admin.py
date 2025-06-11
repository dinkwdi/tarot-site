from django.contrib import admin
from .models import TarotCard, Reading, DrawnCard

@admin.register(TarotCard)
class TarotCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "Нет изображения"
    image_preview.allow_tags = True
    image_preview.short_description = "Превью"

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    list_filter = ('created_at',)

@admin.register(DrawnCard)
class DrawnCardAdmin(admin.ModelAdmin):
    list_display = ('card', 'reading', 'reversed')
    list_filter = ('reversed',)