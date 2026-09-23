    def _redo_transform_rel_fig(self, bbox=None):
        """
        Make the transSubfigure bbox relative to Figure transform.

        Parameters
        ----------
        bbox : bbox or None
            If not None, then the bbox is used for relative bounding box.
            Otherwise it is calculated from the subplotspec.
        """

        if bbox is not None:
            self.bbox_relative.p0 = bbox.p0
            self.bbox_relative.p1 = bbox.p1
            return

        gs = self._subplotspec.get_gridspec()
        # need to figure out *where* this subplotspec is.
        wr = gs.get_width_ratios()
        hr = gs.get_height_ratios()
        nrows, ncols = gs.get_geometry()
        if wr is None:
            wr = np.ones(ncols)
        else:
            wr = np.array(wr)
        if hr is None:
            hr = np.ones(nrows)
        else:
            hr = np.array(hr)
        widthf = np.sum(wr[self._subplotspec.colspan]) / np.sum(wr)
        heightf = np.sum(hr[self._subplotspec.rowspan]) / np.sum(hr)

        x0 = 0
        if not self._subplotspec.is_first_col():
            x0 += np.sum(wr[:self._subplotspec.colspan.start]) / np.sum(wr)

        y0 = 0
        if not self._subplotspec.is_last_row():
            y0 += 1 - (np.sum(hr[:self._subplotspec.rowspan.stop]) /
                       np.sum(hr))

        if self.bbox_relative is None:
            self.bbox_relative = Bbox.from_bounds(x0, y0, widthf, heightf)
        else:
            self.bbox_relative.p0 = (x0, y0)
            self.bbox_relative.p1 = (x0 + widthf, y0 + heightf)
