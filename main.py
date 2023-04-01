def uppercase_decorator(function):
    """
    :rtype: wrapper
    """
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper

def say_hi():
    return 'hello there'


decorate = uppercase_decorator(say_hi)
print(decorate())
