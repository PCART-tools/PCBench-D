    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast("float **", self.image32)
