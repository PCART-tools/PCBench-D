    def __init__(
        self,
        key=None,
        level=None,
        freq=None,
        axis: int = 0,
        sort: bool = False,
        dropna: bool = True,
    ) -> None:
        self.key = key
        self.level = level
        self.freq = freq
        self.axis = axis
        self.sort = sort
        self.dropna = dropna

        self.grouper = None
        self._gpr_index = None
        self.obj = None
        self.indexer = None
        self.binner = None
        self._grouper = None
        self._indexer = None
