    def __init__(self, name):
        if name not in _mathops:
            raise ValueError(
                "\"{0}\" is not a supported function".format(name))
        self.name = name
        self.func = getattr(np, name)
