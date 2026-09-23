    def __setitem__(
        self,
        key: Union[int, Sequence[int], Sequence[bool], slice],
        value: Union[NaTType, Any, Sequence[Any]],
    ) -> None:
        # I'm fudging the types a bit here. "Any" above really depends
        # on type(self). For PeriodArray, it's Period (or stuff coercible
        # to a period in from_sequence). For DatetimeArray, it's Timestamp...
        # I don't know if mypy can do that, possibly with Generics.
        # https://mypy.readthedocs.io/en/latest/generics.html
        if is_list_like(value):
            is_slice = isinstance(key, slice)

            if lib.is_scalar(key):
                raise ValueError("setting an array element with a sequence.")

            if not is_slice:
                key = cast(Sequence, key)
                if len(key) != len(value) and not com.is_bool_indexer(key):
                    msg = (
                        f"shape mismatch: value array of length '{len(key)}' "
                        "does not match indexing result of length "
                        f"'{len(value)}'."
                    )
                    raise ValueError(msg)
                elif not len(key):
                    return

        value = self._validate_setitem_value(value)
        key = check_array_indexer(self, key)
        self._data[key] = value
        self._maybe_clear_freq()
