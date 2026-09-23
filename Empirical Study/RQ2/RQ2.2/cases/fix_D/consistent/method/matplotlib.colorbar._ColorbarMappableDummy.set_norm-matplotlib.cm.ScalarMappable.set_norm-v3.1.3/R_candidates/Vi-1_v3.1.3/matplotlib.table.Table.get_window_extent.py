    def get_window_extent(self, renderer):
        """Return the bounding box of the table in window coords."""
        boxes = [cell.get_window_extent(renderer)
                 for cell in self._cells.values()]
        return Bbox.union(boxes)
