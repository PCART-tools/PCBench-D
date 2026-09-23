    def _get_cython_func_type(self, func: str) -> Callable:
        """
        Return a variable or fixed cython function type.

        Variable algorithms do not use window while fixed do.
        """
        if self.is_freq_type or isinstance(self.window, BaseIndexer):
            return self._get_roll_func(f"{func}_variable")
        return partial(self._get_roll_func(f"{func}_fixed"), win=self._get_window())
