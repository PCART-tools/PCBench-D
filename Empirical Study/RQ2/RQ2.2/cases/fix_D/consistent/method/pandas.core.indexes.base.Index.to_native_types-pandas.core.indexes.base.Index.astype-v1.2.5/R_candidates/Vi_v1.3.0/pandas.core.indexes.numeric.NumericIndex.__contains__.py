    def __contains__(self, key) -> bool:
        """
        Check if key is a float and has a decimal. If it has, return False.
        """
        if not is_integer_dtype(self.dtype):
            return super().__contains__(key)

        hash(key)
        try:
            if is_float(key) and int(key) != key:
                # otherwise the `key in self._engine` check casts e.g. 1.1 -> 1
                return False
            return key in self._engine
        except (OverflowError, TypeError, ValueError):
            return False
