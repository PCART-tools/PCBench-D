    def set_data(self, A):
        """Set the image array."""
        cm.ScalarMappable.set_array(self,
                                    cbook.safe_masked_invalid(A, copy=True))
        self.stale = True
