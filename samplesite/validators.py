from django.core.exceptions import ValidationError


class NoForbiddenCharsValidator:
    def __init__(self, forbidden_chars=(' ',)):
        self.forbidden_chars = forbidden_chars

    def validate(self, password, user=None):
        for fc in self.forbidden_chars:
            if fc in password:
                raise ValidationError(
                    'Пароль не должен содержать недопустимые символы %s' % ', '.join(self.forbidden_chars),
                    code='forbidden_chars_present')

    def get_help_text(self):
        return 'Пароль не должен содержать недопустимые символы %s' % ', '.join(self.forbidden_chars)
