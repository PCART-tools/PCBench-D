    def __contains__(self, key) -> bool:
        """
        Check if key is a float and has a decimal. If it has, return False.
        """
        hash(key)
        try:
            if is_float(key) and int(key) != key:
                return False
            return key in self._engine
        except (OverflowError, TypeError, ValueError):
            return False
