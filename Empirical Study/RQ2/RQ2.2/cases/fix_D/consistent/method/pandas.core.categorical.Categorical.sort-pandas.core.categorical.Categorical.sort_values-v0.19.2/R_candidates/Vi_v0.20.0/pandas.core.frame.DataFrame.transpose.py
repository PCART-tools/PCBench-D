    def transpose(self, *args, **kwargs):
        """Transpose index and columns"""
        nv.validate_transpose(args, dict())
        return super(DataFrame, self).transpose(1, 0, **kwargs)
