    def get_offset(self, width, height, xdescent, ydescent, renderer):
        """
        Get the offset

        accepts extent of the box
        """
        return (self._offset(width, height, xdescent, ydescent, renderer)
                if callable(self._offset)
                else self._offset)
