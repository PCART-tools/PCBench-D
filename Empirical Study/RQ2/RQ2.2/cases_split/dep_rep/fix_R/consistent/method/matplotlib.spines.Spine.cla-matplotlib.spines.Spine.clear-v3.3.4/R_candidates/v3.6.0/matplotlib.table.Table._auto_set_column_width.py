    def _auto_set_column_width(self, col, renderer):
        """Automatically set width for column."""
        cells = [cell for key, cell in self._cells.items() if key[1] == col]
        max_width = max((cell.get_required_width(renderer) for cell in cells),
                        default=0)
        for cell in cells:
            cell.set_width(max_width)
