    def get_tightbbox(self, renderer, call_axes_locator=True,
                      bbox_extra_artists=None, *, for_layout_only=False):
        """
        Return the tight bounding box of the axes, including axis and their
        decorators (xlabel, title, etc).

        Artists that have ``artist.set_in_layout(False)`` are not included
        in the bbox.

        Parameters
        ----------
        renderer : `.RendererBase` subclass
            renderer that will be used to draw the figures (i.e.
            ``fig.canvas.get_renderer()``)

        bbox_extra_artists : list of `.Artist` or ``None``
            List of artists to include in the tight bounding box.  If
            ``None`` (default), then all artist children of the axes are
            included in the tight bounding box.

        call_axes_locator : bool, default: True
            If *call_axes_locator* is ``False``, it does not call the
            ``_axes_locator`` attribute, which is necessary to get the correct
            bounding box. ``call_axes_locator=False`` can be used if the
            caller is only interested in the relative size of the tightbbox
            compared to the axes bbox.

        for_layout_only : default: False
            The bounding box will *not* include the x-extent of the title and
            the xlabel, or the y-extent of the ylabel.

        Returns
        -------
        `.BboxBase`
            Bounding box in figure pixel coordinates.

        See Also
        --------
        matplotlib.axes.Axes.get_window_extent
        matplotlib.axis.Axis.get_tightbbox
        matplotlib.spines.Spine.get_window_extent
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

        if self.axison:
            if self.xaxis.get_visible():
                try:
                    bb_xaxis = self.xaxis.get_tightbbox(
                        renderer, for_layout_only=for_layout_only)
                except TypeError:
                    # in case downstream library has redefined axis:
                    bb_xaxis = self.xaxis.get_tightbbox(renderer)
                if bb_xaxis:
                    bb.append(bb_xaxis)
            if self.yaxis.get_visible():
                try:
                    bb_yaxis = self.yaxis.get_tightbbox(
                        renderer, for_layout_only=for_layout_only)
                except TypeError:
                    # in case downstream library has redefined axis:
                    bb_yaxis = self.yaxis.get_tightbbox(renderer)
                if bb_yaxis:
                    bb.append(bb_yaxis)
        self._update_title_position(renderer)
        axbbox = self.get_window_extent(renderer)
        bb.append(axbbox)

        for title in [self.title, self._left_title, self._right_title]:
            if title.get_visible():
                bt = title.get_window_extent(renderer)
                if for_layout_only and bt.width > 0:
                    # make the title bbox 1 pixel wide so its width
                    # is not accounted for in bbox calculations in
                    # tight/constrained_layout
                    bt.x0 = (bt.x0 + bt.x1) / 2 - 0.5
                    bt.x1 = bt.x0 + 1.0
                bb.append(bt)

        bbox_artists = bbox_extra_artists
        if bbox_artists is None:
            bbox_artists = self.get_default_bbox_extra_artists()

        for a in bbox_artists:
            # Extra check here to quickly see if clipping is on and
            # contained in the axes.  If it is, don't get the tightbbox for
            # this artist because this can be expensive:
            clip_extent = a._get_clipping_extent_bbox()
            if clip_extent is not None:
                clip_extent = mtransforms.Bbox.intersection(
                    clip_extent, axbbox)
                if np.all(clip_extent.extents == axbbox.extents):
                    # clip extent is inside the axes bbox so don't check
                    # this artist
                    continue
            bbox = a.get_tightbbox(renderer)
            if (bbox is not None
                    and 0 < bbox.width < np.inf
                    and 0 < bbox.height < np.inf):
                bb.append(bbox)
        return mtransforms.Bbox.union(
            [b for b in bb if b.width != 0 or b.height != 0])
