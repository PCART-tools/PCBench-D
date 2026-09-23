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

    @_check_savefig_extra_args
    def _print_image(self, filetype, filename):
        origBitmap = self.bitmap

        self.bitmap = wx.Bitmap(math.ceil(self.figure.bbox.width),
                                math.ceil(self.figure.bbox.height))
        renderer = RendererWx(self.bitmap, self.figure.dpi)

        gc = renderer.new_gc()
        self.figure.draw(renderer)

        # image is the object that we call SaveFile on.
        image = self.bitmap

        # Now that we have rendered into the bitmap, save it to the appropriate
        # file type and clean up.
        if (cbook.is_writable_file_like(filename) and
                not isinstance(image, wx.Image)):
            image = image.ConvertToImage()
        if not image.SaveFile(filename, filetype):
            raise RuntimeError(f'Could not save figure to {filename}')

        # Restore everything to normal
        self.bitmap = origBitmap

        # Note: draw is required here since bits of state about the
        # last renderer are strewn about the artist draw methods.  Do
        # not remove the draw without first verifying that these have
        # been cleaned up.  The artist contains() methods will fail
        # otherwise.
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
