    def isowner(self, o):
        """Return whether *o* owns this lock."""
        return self._owner is o
