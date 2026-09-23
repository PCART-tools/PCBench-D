    def get_tightbbox(self, renderer, call_axes_locator=True,
            bbox_extra_artists=None):
        """
        Return the tight bounding box of the axes, including axis and their
        decorators (xlabel, title, etc).

        Artists that have ``artist.set_in_layout(False)`` are not included
        in the bbox.

        Parameters
        ----------
        renderer : `.RendererBase` instance
            renderer that will be used to draw the figures (i.e.
            ``fig.canvas.get_renderer()``)

        bbox_extra_artists : list of `.Artist` or ``None``
            List of artists to include in the tight bounding box.  If
            ``None`` (default), then all artist children of the axes are
            included in the tight bounding box.

        call_axes_locator : boolean (default ``True``)
            If *call_axes_locator* is ``False``, it does not call the
            ``_axes_locator`` attribute, which is necessary to get the correct
            bounding box. ``call_axes_locator=False`` can be used if the
            caller is only interested in the relative size of the tightbbox
            compared to the axes bbox.

        Returns
        -------
        bbox : `.BboxBase`
            bounding box in figure pixel coordinates.
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

        bb_xaxis = self.xaxis.get_tightbbox(renderer)
        if bb_xaxis:
            bb.append(bb_xaxis)

        self._update_title_position(renderer)
        bb.append(self.get_window_extent(renderer))

        if self.title.get_visible():
            bb.append(self.title.get_window_extent(renderer))
        if self._left_title.get_visible():
            bb.append(self._left_title.get_window_extent(renderer))
        if self._right_title.get_visible():
            bb.append(self._right_title.get_window_extent(renderer))

        bb_yaxis = self.yaxis.get_tightbbox(renderer)
        if bb_yaxis:
            bb.append(bb_yaxis)

        bbox_artists = bbox_extra_artists
        if bbox_artists is None:
            bbox_artists = self.get_default_bbox_extra_artists()

        for a in bbox_artists:
            bbox = a.get_tightbbox(renderer)
            if bbox is not None and (bbox.width != 0 or bbox.height != 0):
                bb.append(bbox)

        _bbox = mtransforms.Bbox.union(
            [b for b in bb if b.width != 0 or b.height != 0])

        return _bbox
