    def locked(self):
        """Return whether the lock is currently held by an owner."""
        return self._owner is not None
