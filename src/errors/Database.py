class DatabaseNotUnique(Exception):
    def __init__(self, error):
        super().__init__(error)

class DatabaseInvalid(Exception):
    def __init__(self, error):
        super().__init__(error)

class DatabaseExecutionError(Exception):
    def __init__(self, error):
        super().__init__(error)

class DatabaseInsertError(Exception):
    def __init__(self, error):
        super().__init__(error)

class DatabaseInternalError(Exception):
    def __init__(self, error):
        super().__init__(error)