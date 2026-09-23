    def load_end(self):
        if self._tile_orientation:
            method = {
                2: Image.Transpose.FLIP_LEFT_RIGHT,
                3: Image.Transpose.ROTATE_180,
                4: Image.Transpose.FLIP_TOP_BOTTOM,
                5: Image.Transpose.TRANSPOSE,
                6: Image.Transpose.ROTATE_270,
                7: Image.Transpose.TRANSVERSE,
                8: Image.Transpose.ROTATE_90,
            }.get(self._tile_orientation)
            if method is not None:
                self.im = self.im.transpose(method)
                self._size = self.im.size

        # allow closing if we're on the first frame, there's no next
        # This is the ImageFile.load path only, libtiff specific below.
        if not self.is_animated:
            self._close_exclusive_fp_after_loading = True

            # reset buffered io handle in case fp
            # was passed to libtiff, invalidating the buffer
            self.fp.tell()

            # load IFD data from fp before it is closed
            exif = self.getexif()
            for key in TiffTags.TAGS_V2_GROUPS:
                if key not in exif:
                    continue
                exif.get_ifd(key)
