    def _ensure_type(self: T, obj) -> T:
        """Ensure that an object has same type as self.

        Used by type checkers.
        """
        assert isinstance(obj, type(self)), type(obj)
        return obj
