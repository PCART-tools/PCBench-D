    def _set_view_from_bbox(self, bbox, direction='in',
                            mode=None, twinx=False, twiny=False):
        """
        Update view from a selection bbox.

        .. note::

            Intended to be overridden by new projection types, but if not, the
            default implementation sets the view limits to the bbox directly.

        Parameters
        ----------
        bbox : 4-tuple or 3 tuple
            * If bbox is a 4 tuple, it is the selected bounding box limits,
              in *display* coordinates.
            * If bbox is a 3 tuple, it is an (xp, yp, scl) triple, where
              (xp, yp) is the center of zooming and scl the scale factor to
              zoom by.

        direction : str
            The direction to apply the bounding box.
                * `'in'` - The bounding box describes the view directly, i.e.,
                           it zooms in.
                * `'out'` - The bounding box describes the size to make the
                            existing view, i.e., it zooms out.

        mode : str or None
            The selection mode, whether to apply the bounding box in only the
            `'x'` direction, `'y'` direction or both (`None`).

        twinx : bool
            Whether this axis is twinned in the *x*-direction.

        twiny : bool
            Whether this axis is twinned in the *y*-direction.
        """
        new_xbound, new_ybound = self._prepare_view_from_bbox(
            bbox, direction=direction, mode=mode, twinx=twinx, twiny=twiny)
        if not twinx and mode != "y":
            self.set_xbound(new_xbound)
            self.set_autoscalex_on(False)
        if not twiny and mode != "x":
            self.set_ybound(new_ybound)
            self.set_autoscaley_on(False)
