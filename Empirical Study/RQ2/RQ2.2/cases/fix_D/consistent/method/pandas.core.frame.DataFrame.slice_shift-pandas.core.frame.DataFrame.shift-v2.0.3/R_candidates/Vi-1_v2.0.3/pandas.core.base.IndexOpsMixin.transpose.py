    @final
    def transpose(self: _T, *args, **kwargs) -> _T:
        """
        Return the transpose, which is by definition self.

        Returns
        -------
        %(klass)s
        """
        nv.validate_transpose(args, kwargs)
        return self
