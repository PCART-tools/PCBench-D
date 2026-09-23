    def get_wx_font(self, s, prop):
        """
        Return a wx font.  Cache instances in a font dictionary for
        efficiency
        """
        DEBUG_MSG("get_wx_font()", 1, self)

        key = hash(prop)
        fontprop = prop
        fontname = fontprop.get_name()

        font = self.fontd.get(key)
        if font is not None:
            return font

        # Allow use of platform independent and dependent font names
        wxFontname = self.fontnames.get(fontname, wx.ROMAN)
        wxFacename = ''  # Empty => wxPython chooses based on wx_fontname

        # Font colour is determined by the active wx.Pen
        # TODO: It may be wise to cache font information
        size = self.points_to_pixels(fontprop.get_size_in_points())

        font = wx.Font(int(size + 0.5),             # Size
                       wxFontname,                # 'Generic' name
                       self.fontangles[fontprop.get_style()],   # Angle
                       self.fontweights[fontprop.get_weight()],  # Weight
                       False,                     # Underline
                       wxFacename)                # Platform font name

        # cache the font and gc and return it
        self.fontd[key] = font

        return font
