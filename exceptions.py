"""Exceptions"""


class ApiErrorException(Exception):
    """API Error exception"""

    def __init__(self, code: int, status: str, message: str, detail, *args):
        self.code = code
        self.status = status
        self.message = message
        self.detail = detail
        super().__init__(*args)
