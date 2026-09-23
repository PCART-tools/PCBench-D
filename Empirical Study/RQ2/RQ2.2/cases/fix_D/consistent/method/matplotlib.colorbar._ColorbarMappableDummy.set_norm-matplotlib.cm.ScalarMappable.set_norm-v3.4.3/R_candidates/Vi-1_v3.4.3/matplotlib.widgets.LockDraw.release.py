    def release(self, o):
        """Release the lock from *o*."""
        if not self.available(o):
            raise ValueError('you do not own this lock')
        self._owner = None
