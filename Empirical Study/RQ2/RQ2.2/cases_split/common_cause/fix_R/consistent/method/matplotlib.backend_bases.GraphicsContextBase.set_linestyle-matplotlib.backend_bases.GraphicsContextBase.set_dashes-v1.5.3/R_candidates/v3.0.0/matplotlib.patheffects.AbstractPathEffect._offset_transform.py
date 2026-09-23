    def _offset_transform(self, renderer, transform):
        """Apply the offset to the given transform."""
        offset_x = renderer.points_to_pixels(self._offset[0])
        offset_y = renderer.points_to_pixels(self._offset[1])
        return transform + self._offset_trans.clear().translate(offset_x,
                                                                offset_y)
