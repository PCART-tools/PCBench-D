    def __init__(self, value, converted, kind: str):
        assert isinstance(kind, str), kind
        self.value = value
        self.converted = converted
        self.kind = kind
