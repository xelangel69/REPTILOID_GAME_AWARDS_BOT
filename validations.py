from re import match

def is_english(text):
    return bool(match(r'^[A-Za-z0-9 !@#$%^&*(),.?":{}|<>-]+$', text))

def is_russian(text):
    return bool(match(r'^[А-Яа-я0-9 !@#$%^&*(),.?":{}|<>-]+$', text))