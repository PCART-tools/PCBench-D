    def __new__(cls, value=None, name="unknown", type=None, length=None, enum=None):
        return super().__new__(cls, value, name, type, length, enum or {})
