    def _has_no_reference(self, i: int = 0) -> bool:
        """
        Check for column `i` if it has references.
        (whether it references another array or is itself being referenced)
        Returns True if the column has no references.
        """
        return (self.refs is None or self.refs[0] is None) and weakref.getweakrefcount(
            self.blocks[0]
        ) == 0
