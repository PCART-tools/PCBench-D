    def _is_cython_func(self, arg):
        """
        if we define an internal function for this argument, return it
        """
        return self._cython_table.get(arg)
