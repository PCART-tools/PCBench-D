class FigureCanvasWx(_FigureCanvasWxBase):
    # Rendering to a Wx canvas using the deprecated Wx renderer.

    def draw(self, drawDC=None):
        """
        Render the figure using RendererWx instance renderer, or using a
        previously defined renderer if none is specified.
        """
        DEBUG_MSG("draw()", 1, self)
        self.renderer = RendererWx(self.bitmap, self.figure.dpi)
        self.figure.draw(self.renderer)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)

    def print_bmp(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_BMP, *args, **kwargs)

    if not _has_pil:
        def print_jpeg(self, filename, *args, **kwargs):
            return self._print_image(filename, wx.BITMAP_TYPE_JPEG,
                                     *args, **kwargs)
        print_jpg = print_jpeg

    def print_pcx(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_PCX, *args, **kwargs)

    def print_png(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_PNG, *args, **kwargs)

    if not _has_pil:
        def print_tiff(self, filename, *args, **kwargs):
            return self._print_image(filename, wx.BITMAP_TYPE_TIF,
                                     *args, **kwargs)
        print_tif = print_tiff

    def print_xpm(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_XPM, *args, **kwargs)

    def _print_image(self, filename, filetype, *args, **kwargs):
        origBitmap = self.bitmap

        l, b, width, height = self.figure.bbox.bounds
        width = math.ceil(width)
        height = math.ceil(height)

        self.bitmap = wx.Bitmap(width, height)

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
            jpeg_quality = kwargs.get('quality',
                                      rcParams['savefig.jpeg_quality'])
            image = self.bitmap.ConvertToImage()
            image.SetOption(wx.IMAGE_OPTION_QUALITY, str(jpeg_quality))

        # Now that we have rendered into the bitmap, save it
        # to the appropriate file type and clean up
        if isinstance(filename, str):
            if not image.SaveFile(filename, filetype):
                DEBUG_MSG('print_figure() file save error', 4, self)
                raise RuntimeError(
                    'Could not save figure to %s\n' %
                    (filename))
        elif is_writable_file_like(filename):
            if not isinstance(image, wx.Image):
                image = image.ConvertToImage()
            if not image.SaveStream(filename, filetype):
                DEBUG_MSG('print_figure() file save error', 4, self)
                raise RuntimeError(
                    'Could not save figure to %s\n' %
                    (filename))

        # Restore everything to normal
        self.bitmap = origBitmap

        # Note: draw is required here since bits of state about the
        # last renderer are strewn about the artist draw methods.  Do
        # not remove the draw without first verifying that these have
        # been cleaned up.  The artist contains() methods will fail
        # otherwise.
        if self._isDrawn:
            self.draw()
        self.Refresh()
