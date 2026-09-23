    def __init__(self, base):
        if base <= 0:
            raise ValueError("'base' must be positive")
        self._base = base
