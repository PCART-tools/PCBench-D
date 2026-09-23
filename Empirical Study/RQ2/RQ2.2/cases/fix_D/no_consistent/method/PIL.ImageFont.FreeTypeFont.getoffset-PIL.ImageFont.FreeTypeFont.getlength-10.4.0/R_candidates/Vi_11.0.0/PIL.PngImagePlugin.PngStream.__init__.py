    def __init__(self, fp: IO[bytes]) -> None:
        super().__init__(fp)

        # local copies of Image attributes
        self.im_info: dict[str | tuple[int, int], Any] = {}
        self.im_text: dict[str, str | iTXt] = {}
        self.im_size = (0, 0)
        self.im_mode = ""
        self.im_tile: list[ImageFile._Tile] = []
        self.im_palette: tuple[str, bytes] | None = None
        self.im_custom_mimetype: str | None = None
        self.im_n_frames: int | None = None
        self._seq_num: int | None = None
        self.rewind_state = _RewindState({}, [], None)

        self.text_memory = 0
