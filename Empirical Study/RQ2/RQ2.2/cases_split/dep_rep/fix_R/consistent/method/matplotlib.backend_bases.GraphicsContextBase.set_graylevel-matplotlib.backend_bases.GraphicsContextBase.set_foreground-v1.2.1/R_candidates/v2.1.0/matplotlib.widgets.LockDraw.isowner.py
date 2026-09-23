    def isowner(self, o):
        """Return True if *o* owns this lock"""
        return self._owner is o
