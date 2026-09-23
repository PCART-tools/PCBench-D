    def __init__(self, im: Image.Image) -> None:
        if not hasattr(im, "seek"):
            msg = "im must have seek method"
            raise AttributeError(msg)
        self.im = im
        self.position = getattr(self.im, "_min_frame", 0)
