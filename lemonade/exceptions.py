class LemonadeError(Exception):
    pass


class InvalidKeyError(LemonadeError):
    pass


class InvalidCipherError(LemonadeError):
    pass


class InvalidPathError(LemonadeError):
    pass


class InvalidLemonFileError(LemonadeError):
    pass


class InvalidSourkeyFileError(LemonadeError):
    pass

class IntegrityError(LemonadeError):
    pass