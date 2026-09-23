    def __init__(self, mode: str, *args: Any) -> None:
        self.im: Image.core.ImagingCore | None = None
        self.state = PyCodecState()
        self.fd = None
        self.mode = mode
        self.init(args)
