    def set_fontsize(self, fontsize):
        """
        Set the font size.  May be either a size string, relative to
        the default font size, or an absolute font size in points.

        Parameters
        ----------
        fontsize : {size in points, 'xx-small', 'x-small', 'small', 'medium', \
'large', 'x-large', 'xx-large'}

        See Also
        --------
        .font_manager.FontProperties.set_size
        """
        self._fontproperties.set_size(fontsize)
        self.stale = True
