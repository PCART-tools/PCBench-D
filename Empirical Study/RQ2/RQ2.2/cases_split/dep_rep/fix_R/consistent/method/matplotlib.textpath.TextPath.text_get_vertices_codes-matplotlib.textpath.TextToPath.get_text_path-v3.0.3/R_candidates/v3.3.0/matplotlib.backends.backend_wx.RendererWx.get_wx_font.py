    def get_wx_font(self, s, prop):
        """Return a wx font.  Cache font instances for efficiency."""
        _log.debug("%s - get_wx_font()", type(self))
        key = hash(prop)
        font = self.fontd.get(key)
        if font is not None:
            return font
        # Font colour is determined by the active wx.Pen
        # TODO: It may be wise to cache font information
        self.fontd[key] = font = wx.Font(  # Cache the font and gc.
            pointSize=self.points_to_pixels(prop.get_size_in_points()),
            family=self.fontnames.get(prop.get_name(), wx.ROMAN),
            style=self.fontangles[prop.get_style()],
            weight=self.fontweights[prop.get_weight()])
        return font
