    def get_window_extent(self, renderer):
        bbox = Bbox([[0, 0], [0, 0]])
        trans_data_to_xy = self.get_transform().transform
        bbox.update_from_data_xy(trans_data_to_xy(self.get_xydata()),
                                 ignore=True)
        # correct for marker size, if any
        if self._marker:
            ms = (self._markersize / 72.0 * self.figure.dpi) * 0.5
            bbox = bbox.padded(ms)
        return bbox
