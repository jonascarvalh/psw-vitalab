import string
from random import choice, shuffle

def generate_random_password(size):
    special_chars = string.punctuation
    chars = string.ascii_letters
    numbers_list = string.digits

    qty = size // 3
    if not size % 3 == 0:
        rest = size - (qty*3)
    
    letters = ''
    for i in range(0, qty+rest):
        letters += choice(chars)

    numbers = ''
    for i in range(0, qty):
        numbers += choice(numbers_list)

    specials = ''
    for i in range(0, rest):
        letters += choice(special_chars)
    
    password = list(letters + numbers + specials)
    shuffle(password)

    return ''.join(password)