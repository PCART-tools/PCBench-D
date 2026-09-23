    def __init__(
        self,
        key=None,
        level=None,
        freq=None,
        axis: Axis = 0,
        sort: bool = False,
        dropna: bool = True,
    ) -> None:
        self.key = key
        self.level = level
        self.freq = freq
        self.axis = axis
        self.sort = sort
        self.dropna = dropna

        self._grouper_deprecated = None
        self._indexer_deprecated = None
        self._obj_deprecated = None
        self._gpr_index = None
        self.binner = None
        self._grouper = None
        self._indexer = None
