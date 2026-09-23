    def __init__(self, *args, **kwargs):
        GenericArrayFormatter.__init__(self, *args, **kwargs)

        if self.float_format is not None and self.formatter is None:
            self.formatter = self.float_format
