    def set_foreground(self, fg, isRGBA=False):
        """
        Set the foreground color.  fg can be a MATLAB format string, a
        html hex color string, an rgb or rgba unit tuple, or a float between 0
        and 1.  In the latter case, grayscale is used.

        If you know fg is rgba, set ``isRGBA=True`` for efficiency.
        """
        if self._forced_alpha and isRGBA:
            self._rgb = fg[:3] + (self._alpha,)
        elif self._forced_alpha:
            self._rgb = colors.to_rgba(fg, self._alpha)
        elif isRGBA:
            self._rgb = fg
        else:
            self._rgb = colors.to_rgba(fg)
