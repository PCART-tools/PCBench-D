    def load(self) -> core.PixelAccess | PyAccess.PyAccess | None:
        """
        Allocates storage for the image and loads the pixel data.  In
        normal cases, you don't need to call this method, since the
        Image class automatically loads an opened image when it is
        accessed for the first time.

        If the file associated with the image was opened by Pillow, then this
        method will close it. The exception to this is if the image has
        multiple frames, in which case the file will be left open for seek
        operations. See :ref:`file-handling` for more information.

        :returns: An image access object.
        :rtype: :py:class:`.PixelAccess` or :py:class:`.PyAccess`
        """
        if self.im is not None and self.palette and self.palette.dirty:
            # realize palette
            mode, arr = self.palette.getdata()
            self.im.putpalette(self.palette.mode, mode, arr)
            self.palette.dirty = 0
            self.palette.rawmode = None
            if "transparency" in self.info and mode in ("LA", "PA"):
                if isinstance(self.info["transparency"], int):
                    self.im.putpalettealpha(self.info["transparency"], 0)
                else:
                    self.im.putpalettealphas(self.info["transparency"])
                self.palette.mode = "RGBA"
            else:
                self.palette.palette = self.im.getpalette(
                    self.palette.mode, self.palette.mode
                )

        if self.im is not None:
            if cffi and USE_CFFI_ACCESS:
                if self.pyaccess:
                    return self.pyaccess
                from . import PyAccess

                self.pyaccess = PyAccess.new(self, self.readonly)
                if self.pyaccess:
                    return self.pyaccess
            return self.im.pixel_access(self.readonly)
        return None
