from django.core.cache import cache

from config.settings import CACHE_ENABLED


def get_cache_data(key, model):
    """ Получение низкоурвневого кэша, или загрузка в кэш при отсуствии """

    if CACHE_ENABLED:
        data = cache.get(key)
        if data is None:
            data = model.objects.all()
            cache.set(key, data)
    else:
        data = model.objects.all()

    return data
