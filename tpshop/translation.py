from modeltranslation.translator import register, TranslationOptions
from cities_light.models import City

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name')