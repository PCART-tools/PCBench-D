    def get_width_char(self, c, isord=False):
        """
        Get the width of the character from the character metric WX
        field
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return wx
