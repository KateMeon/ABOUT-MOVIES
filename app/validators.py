from wtforms.validators import StopValidation
from app import get_session
from app.data.users import User


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
        except Exception as error:
            raise StopValidation(
                message=str(error))


class NickValidator:
    """
    Проверяет, что ник не больше 10 символов
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if len(field.data) > 10:
            raise StopValidation(message='Nick must be up to 10 characters')


class MailValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        session = get_session()
        for u in session.query(User).filter(User.email == field.data):
            raise StopValidation("User with this EMail already exist")
