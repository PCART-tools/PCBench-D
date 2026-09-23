    @property
    def _is_immutable(self) -> bool:
        """
        Can arrays with this dtype be modified with __setitem__? If not, return
        True.

        Immutable arrays are expected to raise TypeError on __setitem__ calls.
        """
        return False
