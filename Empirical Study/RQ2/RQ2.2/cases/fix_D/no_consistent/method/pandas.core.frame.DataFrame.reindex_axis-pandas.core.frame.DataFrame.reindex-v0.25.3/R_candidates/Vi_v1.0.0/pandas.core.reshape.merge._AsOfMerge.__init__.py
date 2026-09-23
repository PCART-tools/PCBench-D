    def __init__(
        self,
        left,
        right,
        on=None,
        left_on=None,
        right_on=None,
        left_index: bool = False,
        right_index: bool = False,
        by=None,
        left_by=None,
        right_by=None,
        axis=1,
        suffixes=("_x", "_y"),
        copy: bool = True,
        fill_method=None,
        how: str = "asof",
        tolerance=None,
        allow_exact_matches: bool = True,
        direction: str = "backward",
    ):

        self.by = by
        self.left_by = left_by
        self.right_by = right_by
        self.tolerance = tolerance
        self.allow_exact_matches = allow_exact_matches
        self.direction = direction

        _OrderedMerge.__init__(
            self,
            left,
            right,
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            axis=axis,
            how=how,
            suffixes=suffixes,
            fill_method=fill_method,
        )
