    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast("unsigned short **", self.image)
