    def __init__(
        self,
        left,
        right,
        on=None,
        left_on=None,
        right_on=None,
        left_index=False,
        right_index=False,
        axis=1,
        suffixes=("_x", "_y"),
        copy=True,
        fill_method=None,
        how="outer",
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
