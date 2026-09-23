    def get_tightbbox(self, renderer, call_axes_locator=True):
        """
        Return the tight bounding box of the axes.
        The dimension of the Bbox in canvas coordinate.

        If *call_axes_locator* is *False*, it does not call the
        _axes_locator attribute, which is necessary to get the correct
        bounding box. ``call_axes_locator==False`` can be used if the
        caller is only intereted in the relative size of the tightbbox
        compared to the axes bbox.
        """

        bb = []

        if not self.get_visible():
            return None

        self._set_lims()
        locator = self.get_axes_locator()
        if locator and call_axes_locator:
            pos = locator(self, renderer)
            self.apply_aspect(pos)
        else:
            self.apply_aspect()

        if self._orientation == 'x':
            bb_axis = self.xaxis.get_tightbbox(renderer)
        else:
            bb_axis = self.yaxis.get_tightbbox(renderer)
        if bb_axis:
            bb.append(bb_axis)

        bb.append(self.get_window_extent(renderer))
        _bbox = mtransforms.Bbox.union(
            [b for b in bb if b.width != 0 or b.height != 0])

        return _bbox
