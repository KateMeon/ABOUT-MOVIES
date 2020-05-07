from wtforms.validators import StopValidation


class LengthError(Exception):
    def __str__(self):
        return "Password must be 9 characters or more"


class DigitError(Exception):
    def __str__(self):
        return "Password must contain numbers"


class SequenceError(Exception):
    def __str__(self):
        return "Password must not contain consecutive characters"


def check_sequence(string):
    data = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю']
    for i in range(1, len(string) - 1):
        line = string[i - 1] + string[i] + string[i + 1]
        for j in data:
            if line in j:
                return False
    return True


def check_password(password):
    if len(password) <= 8:
        raise LengthError()
    elif not any([i.isdigit() for i in list(password)]):
        raise DigitError()
    elif not check_sequence(list(password.lower())):
        raise SequenceError()
    return True


class PasswordValidator:
    """
    Проверяет надёжность пароля
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        try:
            check_password(field.data.strip())
        except Exception as ex:
            raise StopValidation(
                message=str(ex))


class NickValidator:
    """
    Проверяет что ник не больше 15 символов
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if len(field.data) > 15:
            raise StopValidation(message='Nick must be up to 16 characters')


class RepeatPasswordValidator:
    def __init__(self, password, message=None):
        self.message = message
        self.password_field_ = password

    def __call__(self, form, field):
        if field.data != self.password_field_.data:
            raise StopValidation(message="Passwords not match")
