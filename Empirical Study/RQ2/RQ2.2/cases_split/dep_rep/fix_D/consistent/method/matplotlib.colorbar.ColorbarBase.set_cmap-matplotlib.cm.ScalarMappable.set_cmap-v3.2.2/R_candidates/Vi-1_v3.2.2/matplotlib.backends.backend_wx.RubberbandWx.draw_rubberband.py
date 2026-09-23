        def draw_rubberband(self, x0, y0, x1, y1):
            dc = wx.ClientDC(self.canvas)
            # this would be required if the Canvas is a ScrolledWindow,
            # which is not the case for now
            # self.PrepareDC(dc)

            # delete old rubberband
            if self._rect:
                self.remove_rubberband(dc)

            # draw new rubberband
            dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            self._rect = (x0, self.canvas._height-y0, x1-x0, -y1+y0)
            dc.DrawRectangle(self._rect)
