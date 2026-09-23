    def get_offsets(self):
        """Return the offsets for the collection."""
        # This decision is based on how they are initialized above in __init__.
        if self._uniform_offsets is None:
            return self._offsets
        else:
            return self._uniform_offsets
