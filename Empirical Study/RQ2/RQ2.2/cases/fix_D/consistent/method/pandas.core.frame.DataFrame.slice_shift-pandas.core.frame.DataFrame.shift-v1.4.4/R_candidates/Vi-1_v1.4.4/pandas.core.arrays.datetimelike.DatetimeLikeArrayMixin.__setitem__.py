    def __setitem__(  # type: ignore[override]
        self,
        key: int | Sequence[int] | Sequence[bool] | slice,
        value: NaTType | Any | Sequence[Any],
    ) -> None:
        # I'm fudging the types a bit here. "Any" above really depends
        # on type(self). For PeriodArray, it's Period (or stuff coercible
        # to a period in from_sequence). For DatetimeArray, it's Timestamp...
        # I don't know if mypy can do that, possibly with Generics.
        # https://mypy.readthedocs.io/en/latest/generics.html
        no_op = check_setitem_lengths(key, value, self)
        if no_op:
            return

        super().__setitem__(key, value)
        self._maybe_clear_freq()
