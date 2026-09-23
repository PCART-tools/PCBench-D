    def __init__(self, *args, **kwargs):
        assert not (len(args) and len(kwargs)), \
                "Only positional or keyword args are allowed"
        self.params = args or kwargs
