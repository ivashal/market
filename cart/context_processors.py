from .views import Cart, ProductCartUser


# def cart(request):
#     return {'cart': Cart(request)}  ## Для того, чтобы функция стала глобальной, ее нужно добавить в settings

def cart(request):
    if request.user.id:  ## Если существует объект user.id (Если пользователь авторизован)
        return {'cart': ProductCartUser(request)}
    
    return {'cart': Cart(request)}
