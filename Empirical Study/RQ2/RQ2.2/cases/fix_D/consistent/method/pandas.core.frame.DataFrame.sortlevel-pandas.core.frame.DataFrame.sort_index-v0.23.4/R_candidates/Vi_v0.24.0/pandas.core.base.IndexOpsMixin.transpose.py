    def transpose(self, *args, **kwargs):
        """
        Return the transpose, which is by definition self.
        """
        nv.validate_transpose(args, kwargs)
        return self
