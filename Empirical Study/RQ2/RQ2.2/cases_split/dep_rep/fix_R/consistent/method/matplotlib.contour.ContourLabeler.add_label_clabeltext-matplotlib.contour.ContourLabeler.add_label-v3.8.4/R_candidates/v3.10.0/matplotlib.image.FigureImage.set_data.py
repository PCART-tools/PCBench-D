    def set_data(self, A):
        """Set the image array."""
        super().set_data(A)
        self.stale = True
