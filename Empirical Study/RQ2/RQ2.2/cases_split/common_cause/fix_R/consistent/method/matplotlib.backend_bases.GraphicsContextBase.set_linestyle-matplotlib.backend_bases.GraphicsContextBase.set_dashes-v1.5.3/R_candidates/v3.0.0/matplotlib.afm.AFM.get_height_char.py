    def get_height_char(self, c, isord=False):
        """Get the bounding box (ink) height of character *c* (space is 0)."""
        if not isord:
            c = ord(c)
        return self._metrics[c].bbox[-1]
