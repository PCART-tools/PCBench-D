    def __init__(self) -> None:
        # FIXME: take "new" parameters / other image?
        # FIXME: turn mode and size into delegating properties?
        self._im: core.ImagingCore | DeferredError | None = None
        self._mode = ""
        self._size = (0, 0)
        self.palette: ImagePalette.ImagePalette | None = None
        self.info: dict[str | tuple[int, int], Any] = {}
        self.readonly = 0
        self._exif: Exif | None = None
