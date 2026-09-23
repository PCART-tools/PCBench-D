    def _is_builtin_func(self, arg):
        """
        if we define an builtin function for this argument, return it,
        otherwise return the arg
        """
        return self._builtin_table.get(arg, arg)
