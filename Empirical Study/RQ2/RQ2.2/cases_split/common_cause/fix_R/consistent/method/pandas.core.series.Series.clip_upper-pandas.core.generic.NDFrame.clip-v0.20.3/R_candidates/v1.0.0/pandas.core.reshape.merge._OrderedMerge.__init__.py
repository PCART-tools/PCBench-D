    def __init__(
        self,
        left,
        right,
        on=None,
        left_on=None,
        right_on=None,
        left_index: bool = False,
        right_index: bool = False,
        axis=1,
        suffixes=("_x", "_y"),
        copy: bool = True,
        fill_method=None,
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
