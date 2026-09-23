    def __init__(
        self,
        mode: str,
        bands: tuple[str, ...],
        basemode: str,
        basetype: str,
        typestr: str,
    ) -> None:
        self.mode = mode
        self.bands = bands
        self.basemode = basemode
        self.basetype = basetype
        self.typestr = typestr
