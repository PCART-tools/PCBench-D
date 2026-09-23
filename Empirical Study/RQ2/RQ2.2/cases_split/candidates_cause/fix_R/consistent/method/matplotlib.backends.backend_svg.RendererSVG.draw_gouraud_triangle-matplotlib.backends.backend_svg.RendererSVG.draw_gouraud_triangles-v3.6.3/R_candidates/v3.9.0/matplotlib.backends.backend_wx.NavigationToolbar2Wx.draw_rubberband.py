    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        sf = 1 if wx.Platform == '__WXMSW__' else self.canvas.GetDPIScaleFactor()
        self.canvas._rubberband_rect = (x0/sf, (height - y0)/sf,
                                        x1/sf, (height - y1)/sf)
        self.canvas.Refresh()
