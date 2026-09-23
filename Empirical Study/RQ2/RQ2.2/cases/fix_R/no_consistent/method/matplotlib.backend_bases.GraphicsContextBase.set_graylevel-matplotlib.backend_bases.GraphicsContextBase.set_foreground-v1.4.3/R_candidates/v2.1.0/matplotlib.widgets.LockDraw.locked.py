    def locked(self):
        """Return True if the lock is currently held by an owner"""
        return self._owner is not None
