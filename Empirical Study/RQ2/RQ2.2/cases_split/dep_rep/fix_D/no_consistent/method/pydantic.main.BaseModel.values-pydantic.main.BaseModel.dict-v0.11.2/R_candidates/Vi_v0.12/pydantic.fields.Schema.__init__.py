    def __init__(self, default, *, alias=None, title=None, choice_names=None, **extra):
        self.default = default
        self.alias = alias
        self.title = title
        self.choice_names = choice_names
        self.extra = extra
