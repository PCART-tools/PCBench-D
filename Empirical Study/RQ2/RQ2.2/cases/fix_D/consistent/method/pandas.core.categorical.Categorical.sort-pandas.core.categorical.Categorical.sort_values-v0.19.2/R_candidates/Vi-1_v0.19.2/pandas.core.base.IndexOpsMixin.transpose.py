    def transpose(self, *args, **kwargs):
        """ return the transpose, which is by definition self """
        nv.validate_transpose(args, kwargs)
        return self
