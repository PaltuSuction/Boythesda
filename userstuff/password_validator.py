from django.core.exceptions import ValidationError

class CustomPasswordValidator():

    def validate(self, password, user = None):
        if not any(char.isdigit() for char in password):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру!')
        if not any(char.isupper for char in password):
            raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву!')
        if len(password) < 5:
            gay = len(password)
            raise ValidationError('Пароль должен быть длиннее пяти символов!')

    def get_help_text(self):
        return 'Пароль должен содержать хотя бы одну заглавную букву, одну цифру и быть длинее пяти символов.'