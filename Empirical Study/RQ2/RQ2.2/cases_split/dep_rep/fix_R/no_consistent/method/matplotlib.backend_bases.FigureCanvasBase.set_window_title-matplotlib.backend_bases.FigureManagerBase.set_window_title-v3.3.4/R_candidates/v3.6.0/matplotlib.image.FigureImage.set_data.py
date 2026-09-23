    def set_data(self, A):
        """Set the image array."""
        cm.ScalarMappable.set_array(self, A)
        self.stale = True
