    def __init__(
        self,
        left: DataFrame | Series,
        right: DataFrame | Series,
        on: IndexLabel | None = None,
        left_on: IndexLabel | None = None,
        right_on: IndexLabel | None = None,
        left_index: bool = False,
        right_index: bool = False,
        axis: int = 1,
        suffixes: Suffixes = ("_x", "_y"),
        copy: bool = True,
        fill_method: str | None = None,
        how: str = "outer",
    ):

        self.fill_method = fill_method
        _MergeOperation.__init__(
            self,
            left,
            right,
            on=on,
            left_on=left_on,
            left_index=left_index,
            right_index=right_index,
            right_on=right_on,
            axis=axis,
            how=how,
            suffixes=suffixes,
            sort=True,  # factorize sorts
        )
