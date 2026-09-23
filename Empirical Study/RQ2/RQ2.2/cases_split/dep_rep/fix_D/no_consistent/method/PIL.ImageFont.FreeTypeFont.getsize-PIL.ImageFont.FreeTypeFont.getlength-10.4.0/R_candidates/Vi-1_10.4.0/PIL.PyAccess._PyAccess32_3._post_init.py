    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast("struct Pixel_RGBA **", self.image32)
