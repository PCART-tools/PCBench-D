    def __init__(self, img: Image.Image, readonly: bool = False) -> None:
        deprecate("PyAccess", 11)
        vals = dict(img.im.unsafe_ptrs)
        self.readonly = readonly
        self.image8 = ffi.cast("unsigned char **", vals["image8"])
        self.image32 = ffi.cast("int **", vals["image32"])
        self.image = ffi.cast("unsigned char **", vals["image"])
        self.xsize, self.ysize = img.im.size
        self._img = img

        # Keep pointer to im object to prevent dereferencing.
        self._im = img.im
        if self._im.mode in ("P", "PA"):
            self._palette = img.palette

        # Debugging is polluting test traces, only useful here
        # when hacking on PyAccess
        # logger.debug("%s", vals)
        self._post_init()
