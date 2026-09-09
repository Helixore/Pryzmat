from rest_framework.exceptions import ValidationError
import re


def validate_pesel(value: str) -> None:
    """Walidator PESEL do użycia w modelu Django (np. w polu PESEL)."""
    if not re.fullmatch(r'\d{11}', value):
        raise ValidationError('PESEL musi składać się z dokładnie 11 cyfr.')

    weights = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
    checksum = sum(int(d) * w for d, w in zip(value[:10], weights)) % 10
    control_digit = (10 - checksum) % 10

    if control_digit != int(value[10]):
        raise ValidationError('Nieprawidłowa cyfra kontrolna PESEL.')

def validate_grade(value: float):
    if not value > 0 and value < 6:
        raise ValidationError("Nieprawidłowa ocena.")