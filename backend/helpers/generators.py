import random, string

def return_registration_code(length=32):
    """Generates a random registration code of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))