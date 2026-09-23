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
