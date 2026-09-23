    def _formatter_func(self, tup):
        """
        Formats each item in tup according to its level's formatter function.
        """
        formatter_funcs = [level._formatter_func for level in self.levels]
        return tuple(func(val) for func, val in zip(formatter_funcs, tup))
