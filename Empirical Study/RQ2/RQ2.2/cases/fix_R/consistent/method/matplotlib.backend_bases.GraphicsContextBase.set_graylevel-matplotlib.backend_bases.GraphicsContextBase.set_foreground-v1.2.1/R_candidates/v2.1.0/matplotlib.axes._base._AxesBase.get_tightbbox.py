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

        locator = self.get_axes_locator()
        if locator and call_axes_locator:
            pos = locator(self, renderer)
            self.apply_aspect(pos)
        else:
            self.apply_aspect()

        bb.append(self.get_window_extent(renderer))

        if self.title.get_visible():
            bb.append(self.title.get_window_extent(renderer))
        if self._left_title.get_visible():
            bb.append(self._left_title.get_window_extent(renderer))
        if self._right_title.get_visible():
            bb.append(self._right_title.get_window_extent(renderer))

        bb_xaxis = self.xaxis.get_tightbbox(renderer)
        if bb_xaxis:
            bb.append(bb_xaxis)

        bb_yaxis = self.yaxis.get_tightbbox(renderer)
        if bb_yaxis:
            bb.append(bb_yaxis)

        for child in self.get_children():
            if isinstance(child, OffsetBox) and child.get_visible():
                bb.append(child.get_window_extent(renderer))

        _bbox = mtransforms.Bbox.union(
            [b for b in bb if b.width != 0 or b.height != 0])

        return _bbox
