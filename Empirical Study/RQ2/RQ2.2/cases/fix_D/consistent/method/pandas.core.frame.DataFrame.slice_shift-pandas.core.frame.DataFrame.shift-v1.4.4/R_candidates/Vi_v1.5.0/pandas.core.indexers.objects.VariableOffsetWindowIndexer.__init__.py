    def __init__(
        self,
        index_array: np.ndarray | None = None,
        window_size: int = 0,
        index=None,
        offset=None,
        **kwargs,
    ) -> None:
        super().__init__(index_array, window_size, **kwargs)
        self.index = index
        self.offset = offset
