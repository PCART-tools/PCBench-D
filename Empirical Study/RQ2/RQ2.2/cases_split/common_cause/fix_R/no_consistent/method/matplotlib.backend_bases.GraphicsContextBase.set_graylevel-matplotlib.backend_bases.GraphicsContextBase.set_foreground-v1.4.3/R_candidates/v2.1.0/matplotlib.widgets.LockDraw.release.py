    def release(self, o):
        """release the lock"""
        if not self.available(o):
            raise ValueError('you do not own this lock')
        self._owner = None
