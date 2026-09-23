    def __init__(
        self,
        data: FrameOrSeriesUnion,
        uuid: str | None = None,
        uuid_len: int = 5,
        table_styles: CSSStyles | None = None,
        table_attributes: str | None = None,
        caption: str | tuple | None = None,
        cell_ids: bool = True,
    ):

        # validate ordered args
        if isinstance(data, Series):
            data = data.to_frame()
        if not isinstance(data, DataFrame):
            raise TypeError("``data`` must be a Series or DataFrame")
        self.data: DataFrame = data
        self.index: Index = data.index
        self.columns: Index = data.columns
        if not isinstance(uuid_len, int) or not uuid_len >= 0:
            raise TypeError("``uuid_len`` must be an integer in range [0, 32].")
        self.uuid_len = min(32, uuid_len)
        self.uuid = (uuid or uuid4().hex[: self.uuid_len]) + "_"
        self.table_styles = table_styles
        self.table_attributes = table_attributes
        self.caption = caption
        self.cell_ids = cell_ids

        # add rendering variables
        self.hide_index_: bool = False  # bools for hiding col/row headers
        self.hide_columns_: bool = False
        self.hidden_rows: Sequence[int] = []  # sequence for specific hidden rows/cols
        self.hidden_columns: Sequence[int] = []
        self.ctx: DefaultDict[tuple[int, int], CSSList] = defaultdict(list)
        self.cell_context: DefaultDict[tuple[int, int], str] = defaultdict(str)
        self._todo: list[tuple[Callable, tuple, dict]] = []
        self.tooltips: Tooltips | None = None
        def_precision = get_option("display.precision")
        self._display_funcs: DefaultDict[  # maps (row, col) -> formatting function
            tuple[int, int], Callable[[Any], str]
        ] = defaultdict(lambda: partial(_default_formatter, precision=def_precision))
