class Error(Exception):
    class UnknownError(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class BaseError(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class TestException(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class ResponseError(BaseError, Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class ParameterError(BaseError, Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class TerminalError(BaseError, Exception):
        def __init__(self, *args):
            super().__init__(*args)
