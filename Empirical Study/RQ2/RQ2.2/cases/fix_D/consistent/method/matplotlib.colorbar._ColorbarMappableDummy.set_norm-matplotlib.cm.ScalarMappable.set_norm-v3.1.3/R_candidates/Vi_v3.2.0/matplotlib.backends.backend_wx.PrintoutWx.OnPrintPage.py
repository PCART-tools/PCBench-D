    def OnPrintPage(self, page):
        self.canvas.draw()

        dc = self.GetDC()
        ppw, pph = self.GetPPIPrinter()      # printer's pixels per in
        pgw, pgh = self.GetPageSizePixels()  # page size in pixels
        dcw, dch = dc.GetSize()
        grw, grh = self.canvas.GetSize()

        # save current figure dpi resolution and bg color,
        # so that we can temporarily set them to the dpi of
        # the printer, and the bg color to white
        bgcolor = self.canvas.figure.get_facecolor()
        fig_dpi = self.canvas.figure.dpi

        # draw the bitmap, scaled appropriately
        vscale = float(ppw) / fig_dpi

        # set figure resolution,bg color for printer
        self.canvas.figure.dpi = ppw
        self.canvas.figure.set_facecolor('#FFFFFF')

        renderer = RendererWx(self.canvas.bitmap, self.canvas.figure.dpi)
        self.canvas.figure.draw(renderer)
        self.canvas.bitmap.SetWidth(
            int(self.canvas.bitmap.GetWidth() * vscale))
        self.canvas.bitmap.SetHeight(
            int(self.canvas.bitmap.GetHeight() * vscale))
        self.canvas.draw()

        # page may need additional scaling on preview
        page_scale = 1.0
        if self.IsPreview():
            page_scale = float(dcw) / pgw

        # get margin in pixels = (margin in in) * (pixels/in)
        top_margin = int(self.margin * pph * page_scale)
        left_margin = int(self.margin * ppw * page_scale)

        # set scale so that width of output is self.width inches
        # (assuming grw is size of graph in inches....)
        user_scale = (self.width * fig_dpi * page_scale) / float(grw)

        dc.SetDeviceOrigin(left_margin, top_margin)
        dc.SetUserScale(user_scale, user_scale)

        # this cute little number avoid API inconsistencies in wx
        try:
            dc.DrawBitmap(self.canvas.bitmap, 0, 0)
        except Exception:
            try:
                dc.DrawBitmap(self.canvas.bitmap, (0, 0))
            except Exception:
                pass

        # restore original figure  resolution
        self.canvas.figure.set_facecolor(bgcolor)
        self.canvas.figure.dpi = fig_dpi
        self.canvas.draw()
        return True
