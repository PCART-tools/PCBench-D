    def __setstate__(self, state: list[Any]) -> None:
        path, size, index, encoding, layout_engine = state
        FreeTypeFont.__init__(self, path, size, index, encoding, layout_engine)
