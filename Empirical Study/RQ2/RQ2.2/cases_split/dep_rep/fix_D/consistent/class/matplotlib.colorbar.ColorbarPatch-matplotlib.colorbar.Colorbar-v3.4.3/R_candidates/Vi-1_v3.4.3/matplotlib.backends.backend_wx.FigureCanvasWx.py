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

    def print_bmp(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_BMP, *args, **kwargs)

    def print_jpeg(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_JPEG,
                                 *args, **kwargs)
    print_jpg = print_jpeg

    def print_pcx(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_PCX, *args, **kwargs)

    def print_png(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_PNG, *args, **kwargs)

    def print_tiff(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_TIF, *args, **kwargs)
    print_tif = print_tiff

    def print_xpm(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_XPM, *args, **kwargs)

    @_check_savefig_extra_args
    def _print_image(self, filename, filetype, *, quality=None):
        origBitmap = self.bitmap

        self.bitmap = wx.Bitmap(math.ceil(self.figure.bbox.width),
                                math.ceil(self.figure.bbox.height))
        renderer = RendererWx(self.bitmap, self.figure.dpi)

        gc = renderer.new_gc()
        self.figure.draw(renderer)

        # image is the object that we call SaveFile on.
        image = self.bitmap
        # set the JPEG quality appropriately.  Unfortunately, it is only
        # possible to set the quality on a wx.Image object.  So if we
        # are saving a JPEG, convert the wx.Bitmap to a wx.Image,
        # and set the quality.
        if filetype == wx.BITMAP_TYPE_JPEG:
            if quality is None:
                quality = dict.__getitem__(mpl.rcParams,
                                           'savefig.jpeg_quality')
            image = self.bitmap.ConvertToImage()
            image.SetOption(wx.IMAGE_OPTION_QUALITY, str(quality))

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
