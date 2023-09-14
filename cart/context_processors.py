from .views import Cart


def cart(request):
    return {'cart': Cart(request)}  ## Для того, чтобы функция стала глобальной, ее нужно добавить в settings
