    def _get_grid_bbox(self, renderer):
        """Get a bbox, in axes co-ordinates for the cells.

        Only include those in the range (0,0) to (maxRow, maxCol)"""
        boxes = [cell.get_window_extent(renderer)
                 for (row, col), cell in six.iteritems(self._cells)
                 if row >= 0 and col >= 0]
        bbox = Bbox.union(boxes)
        return bbox.inverse_transformed(self.get_transform())
