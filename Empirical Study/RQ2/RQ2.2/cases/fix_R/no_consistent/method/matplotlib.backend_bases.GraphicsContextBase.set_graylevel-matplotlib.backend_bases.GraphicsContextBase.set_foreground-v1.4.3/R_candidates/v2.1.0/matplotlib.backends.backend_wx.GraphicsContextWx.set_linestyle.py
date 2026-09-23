    @cbook.deprecated("2.1")
    def set_linestyle(self, ls):
        """
        Set the line style to be one of
        """
        DEBUG_MSG("set_linestyle()", 1, self)
        self.select()
        GraphicsContextBase.set_linestyle(self, ls)
        try:
            self._style = wxc.dashd_wx[ls]
        except KeyError:
            self._style = wx.LONG_DASH  # Style not used elsewhere...

        # On MS Windows platform, only line width of 1 allowed for dash lines
        if wx.Platform == '__WXMSW__':
            self.set_linewidth(1)

        self._pen.SetStyle(self._style)
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
