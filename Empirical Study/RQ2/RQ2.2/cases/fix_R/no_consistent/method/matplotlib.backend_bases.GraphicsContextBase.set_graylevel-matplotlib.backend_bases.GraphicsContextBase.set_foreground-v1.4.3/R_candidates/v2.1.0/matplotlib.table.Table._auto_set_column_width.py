    def _auto_set_column_width(self, col, renderer):
        """ Automagically set width for column.
        """
        cells = [key for key in self._cells if key[1] == col]

        # find max width
        width = 0
        for cell in cells:
            c = self._cells[cell]
            width = max(c.get_required_width(renderer), width)

        # Now set the widths
        for cell in cells:
            self._cells[cell].set_width(width)
