class TextArea(OffsetBox):
    """
    The TextArea is a container artist for a single Text instance.

    The text is placed at (0, 0) with baseline+left alignment, by default. The
    width and height of the TextArea instance is the width and height of its
    child text.
    """

    @_api.delete_parameter("3.4", "minimumdescent")
    def __init__(self, s,
                 textprops=None,
                 multilinebaseline=False,
                 minimumdescent=True,
                 ):
        """
        Parameters
        ----------
        s : str
            The text to be displayed.
        textprops : dict, default: {}
            Dictionary of keyword parameters to be passed to the `.Text`
            instance in the TextArea.
        multilinebaseline : bool, default: False
            Whether the baseline for multiline text is adjusted so that it
            is (approximately) center-aligned with single-line text.
        minimumdescent : bool, default: True
            If `True`, the box has a minimum descent of "p".  This is now
            effectively always True.
        """
        if textprops is None:
            textprops = {}
        self._text = mtext.Text(0, 0, s, **textprops)
        super().__init__()
        self._children = [self._text]
        self.offset_transform = mtransforms.Affine2D()
        self._baseline_transform = mtransforms.Affine2D()
        self._text.set_transform(self.offset_transform +
                                 self._baseline_transform)
        self._multilinebaseline = multilinebaseline
        self._minimumdescent = minimumdescent

    def set_text(self, s):
        """Set the text of this area as a string."""
        self._text.set_text(s)
        self.stale = True

    def get_text(self):
        """Return the string representation of this area's text."""
        return self._text.get_text()

    def set_multilinebaseline(self, t):
        """
        Set multilinebaseline.

        If True, the baseline for multiline text is adjusted so that it is
        (approximately) center-aligned with single-line text.  This is used
        e.g. by the legend implementation so that single-line labels are
        baseline-aligned, but multiline labels are "center"-aligned with them.
        """
        self._multilinebaseline = t
        self.stale = True

    def get_multilinebaseline(self):
        """
        Get multilinebaseline.
        """
        return self._multilinebaseline

    @_api.deprecated("3.4")
    def set_minimumdescent(self, t):
        """
        Set minimumdescent.

        If True, extent of the single line text is adjusted so that
        its descent is at least the one of the glyph "p".
        """
        # The current implementation of Text._get_layout always behaves as if
        # this is True.
        self._minimumdescent = t
        self.stale = True

    @_api.deprecated("3.4")
    def get_minimumdescent(self):
        """
        Get minimumdescent.
        """
        return self._minimumdescent

    def set_transform(self, t):
        """
        set_transform is ignored.
        """

    def set_offset(self, xy):
        """
        Set the offset of the container.

        Parameters
        ----------
        xy : (float, float)
            The (x, y) coordinates of the offset in display units.
        """
        self._offset = xy
        self.offset_transform.clear()
        self.offset_transform.translate(xy[0], xy[1])
        self.stale = True

    def get_offset(self):
        """Return offset of the container."""
        return self._offset

    def get_window_extent(self, renderer):
        # docstring inherited
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset()
        return mtransforms.Bbox.from_bounds(ox - xd, oy - yd, w, h)

    def get_extent(self, renderer):
        _, h_, d_ = renderer.get_text_width_height_descent(
            "lp", self._text._fontproperties,
            ismath="TeX" if self._text.get_usetex() else False)

        bbox, info, yd = self._text._get_layout(renderer)
        w, h = bbox.width, bbox.height

        self._baseline_transform.clear()

        if len(info) > 1 and self._multilinebaseline:
            yd_new = 0.5 * h - 0.5 * (h_ - d_)
            self._baseline_transform.translate(0, yd - yd_new)
            yd = yd_new
        else:  # single line
            h_d = max(h_ - d_, h - yd)
            h = h_d + yd

        ha = self._text.get_horizontalalignment()
        if ha == 'left':
            xd = 0
        elif ha == 'center':
            xd = w / 2
        elif ha == 'right':
            xd = w

        return w, h, xd, yd

    def draw(self, renderer):
        # docstring inherited
        self._text.draw(renderer)
        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
