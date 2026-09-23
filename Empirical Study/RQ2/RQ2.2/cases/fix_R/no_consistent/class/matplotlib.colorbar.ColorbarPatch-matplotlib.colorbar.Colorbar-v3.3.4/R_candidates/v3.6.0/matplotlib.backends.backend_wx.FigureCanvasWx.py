class FigureCanvasWx(_FigureCanvasWxBase):
    # Rendering to a Wx canvas using the deprecated Wx renderer.

    def draw(self, drawDC=None):
        """
        Render the figure using RendererWx instance renderer, or using a
        previously defined renderer if none is specified.
        """
        _log.debug("%s - draw()", type(self))
        self.renderer = RendererWx(self.bitmap, self.figure.dpi)
        self.figure.draw(self.renderer)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)

    def _print_image(self, filetype, filename):
        bitmap = wx.Bitmap(math.ceil(self.figure.bbox.width),
                           math.ceil(self.figure.bbox.height))
        self.figure.draw(RendererWx(bitmap, self.figure.dpi))
        saved_obj = (bitmap.ConvertToImage()
                     if cbook.is_writable_file_like(filename)
                     else bitmap)
        if not saved_obj.SaveFile(filename, filetype):
            raise RuntimeError(f'Could not save figure to {filename}')
        # draw() is required here since bits of state about the last renderer
        # are strewn about the artist draw methods.  Do not remove the draw
        # without first verifying that these have been cleaned up.  The artist
        # contains() methods will fail otherwise.
        if self._isDrawn:
            self.draw()
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError if doing things after window is closed.
        if self:
            self.Refresh()

    print_bmp = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_BMP)
    print_jpeg = print_jpg = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_JPEG)
    print_pcx = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_PCX)
    print_png = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_PNG)
    print_tiff = print_tif = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_TIF)
    print_xpm = functools.partialmethod(
        _print_image, wx.BITMAP_TYPE_XPM)
