    def __call__(self, o):
        """reserve the lock for *o*"""
        if not self.available(o):
            raise ValueError('already locked')
        self._owner = o
