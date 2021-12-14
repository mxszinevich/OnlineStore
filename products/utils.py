def is_sessionid(request):
    """
    Метод проверяет наличие sessionid на клиентской стороне
    Нужен при удалении COOKIES на клиенте иначе возникнет исключение
    """
    return bool('sessionid' in request.COOKIES)



