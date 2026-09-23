    def __setitem__(
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

        # Calling super() before the no_op short-circuit means that we raise
        #  on invalid 'value' even if this is a no-op, e.g. wrong-dtype empty array.
        super().__setitem__(key, value)

        if no_op:
            return

        self._maybe_clear_freq()
