    def ensure_not_dirty(self):
        """If dirty, reasks the writers if they are available"""
        if self._dirty:
            self.reset_available_writers()
