    def _on_size(self, event):
        """
        Called when wxEventSize is generated.

        In this application we attempt to resize to fit the window, so it
        is better to take the performance hit and redraw the whole window.
        """
        self._update_device_pixel_ratio()
        _log.debug("%s - _on_size()", type(self))
        sz = self.GetParent().GetSizer()
        if sz:
            si = sz.GetItem(self)
        if sz and si and not si.Proportion and not si.Flag & wx.EXPAND:
            # managed by a sizer, but with a fixed size
            size = self.GetMinSize()
        else:
            # variable size
            size = self.GetClientSize()
            # Do not allow size to become smaller than MinSize
            size.IncTo(self.GetMinSize())
        if getattr(self, "_width", None):
            if size == (self._width, self._height):
                # no change in size
                return
        self._width, self._height = size
        self._isDrawn = False

        if self._width <= 1 or self._height <= 1:
            return  # Empty figure

        # Create a new, correctly sized bitmap
        dpival = self.figure.dpi
        if not wx.Platform == '__WXMSW__':
            scale = self.GetDPIScaleFactor()
            dpival /= scale
        winch = self._width / dpival
        hinch = self._height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        # Rendering will happen on the associated paint event
        # so no need to do anything here except to make sure
        # the whole background is repainted.
        self.Refresh(eraseBackground=False)
        ResizeEvent("resize_event", self)._process()
        self.draw_idle()
