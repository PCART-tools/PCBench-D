    def draw_rubberband(self, event, x0, y0, x1, y1):
        if self.retinaFix:  # On Macs, use the following code
            # wx.DCOverlay does not work properly on Retina displays.
            rubberBandColor = '#C0C0FF'
            if self.prevZoomRect:
                self.prevZoomRect.pop(0).remove()
            self.canvas.restore_region(self.savedRetinaImage)
            X0, X1 = self.zoomStartX, event.xdata
            Y0, Y1 = self.zoomStartY, event.ydata
            lineX = (X0, X0, X1, X1, X0)
            lineY = (Y0, Y1, Y1, Y0, Y0)
            self.prevZoomRect = self.zoomAxes.plot(
                lineX, lineY, '-', color=rubberBandColor)
            self.zoomAxes.draw_artist(self.prevZoomRect[0])
            self.canvas.blit(self.zoomAxes.bbox)
            return

        # Use an Overlay to draw a rubberband-like bounding box.

        dc = wx.ClientDC(self.canvas)
        odc = wx.DCOverlay(self.wxoverlay, dc)
        odc.Clear()

        # Mac's DC is already the same as a GCDC, and it causes
        # problems with the overlay if we try to use an actual
        # wx.GCDC so don't try it.
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)

        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0

        if y1 < y0:
            y0, y1 = y1, y0
        if x1 < x0:
            x0, x1 = x1, x0

        w = x1 - x0
        h = y1 - y0
        rect = wx.Rect(x0, y0, w, h)

        rubberBandColor = '#C0C0FF'  # or load from config?

        # Set a pen for the border
        color = wx.Colour(rubberBandColor)
        dc.SetPen(wx.Pen(color, 1))

        # use the same color, plus alpha for the brush
        r, g, b, a = color.Get(True)
        color.Set(r, g, b, 0x60)
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(rect)
