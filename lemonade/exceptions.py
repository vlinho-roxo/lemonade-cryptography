class LemonadeError(Exception):
    pass


class InvalidKeyError(LemonadeError):
    pass


class InvalidCipherError(LemonadeError):
    pass