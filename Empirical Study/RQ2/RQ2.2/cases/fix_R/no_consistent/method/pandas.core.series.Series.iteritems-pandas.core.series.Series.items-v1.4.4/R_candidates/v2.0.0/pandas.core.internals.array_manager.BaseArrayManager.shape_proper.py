    @property
    def shape_proper(self) -> tuple[int, ...]:
        # this returns (n_rows, n_columns)
        return tuple(len(ax) for ax in self._axes)
