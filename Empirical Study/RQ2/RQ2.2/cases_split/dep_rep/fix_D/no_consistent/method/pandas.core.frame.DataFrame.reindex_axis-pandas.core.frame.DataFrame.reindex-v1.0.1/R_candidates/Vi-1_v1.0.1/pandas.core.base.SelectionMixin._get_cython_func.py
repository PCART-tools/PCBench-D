    def _get_cython_func(self, arg: str) -> Optional[str]:
        """
        if we define an internal function for this argument, return it
        """
        return self._cython_table.get(arg)
