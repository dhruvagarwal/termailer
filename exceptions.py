class IncorrectEmailException(Exception):
    def __init__(self):
        message = """Incorrect email address encountered, expected
                    something like example@domain.com"""
        super(IncorrectEmailException, self).__init__(message)
