    def get_height_char(self, c, isord=False):
        """
        Get the height of character *c* from the bounding box.  This
        is the ink height (space is 0)
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return bbox[-1]
