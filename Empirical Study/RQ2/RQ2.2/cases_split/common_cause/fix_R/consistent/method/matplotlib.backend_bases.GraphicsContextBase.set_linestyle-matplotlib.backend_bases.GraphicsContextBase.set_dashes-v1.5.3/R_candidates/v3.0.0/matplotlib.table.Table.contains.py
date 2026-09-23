    def contains(self, mouseevent):
        """Test whether the mouse event occurred in the table.

        Returns T/F, {}
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)

        # TODO: Return index of the cell containing the cursor so that the user
        # doesn't have to bind to each one individually.
        renderer = self.figure._cachedRenderer
        if renderer is not None:
            boxes = [cell.get_window_extent(renderer)
                     for (row, col), cell in self._cells.items()
                     if row >= 0 and col >= 0]
            bbox = Bbox.union(boxes)
            return bbox.contains(mouseevent.x, mouseevent.y), {}
        else:
            return False, {}
