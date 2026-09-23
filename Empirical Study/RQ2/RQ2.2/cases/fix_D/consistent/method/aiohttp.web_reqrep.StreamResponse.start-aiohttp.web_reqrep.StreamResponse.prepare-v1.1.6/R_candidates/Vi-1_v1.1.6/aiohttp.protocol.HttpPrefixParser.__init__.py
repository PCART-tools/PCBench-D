    def __init__(self, allowed_methods=()):
        self.allowed_methods = [m.upper() for m in allowed_methods]
