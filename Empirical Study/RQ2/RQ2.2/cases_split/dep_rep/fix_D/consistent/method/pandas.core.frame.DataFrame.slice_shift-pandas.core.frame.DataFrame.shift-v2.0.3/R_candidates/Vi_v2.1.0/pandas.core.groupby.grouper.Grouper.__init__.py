    def __init__(
        self,
        key=None,
        level=None,
        freq=None,
        axis: Axis | lib.NoDefault = lib.no_default,
        sort: bool = False,
        dropna: bool = True,
    ) -> None:
        if type(self) is Grouper:
            # i.e. not TimeGrouper
            if axis is not lib.no_default:
                warnings.warn(
                    "Grouper axis keyword is deprecated and will be removed in a "
                    "future version. To group on axis=1, use obj.T.groupby(...) "
                    "instead",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            else:
                axis = 0
        if axis is lib.no_default:
            axis = 0

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
