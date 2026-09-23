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
                        "shape mismatch: value array of length '{}' does "
                        "not match indexing result of length '{}'."
                    )
                    raise ValueError(msg.format(len(key), len(value)))
                elif not len(key):
                    return

            value = type(self)._from_sequence(value, dtype=self.dtype)
            self._check_compatible_with(value)
            value = value.asi8
        elif isinstance(value, self._scalar_type):
            self._check_compatible_with(value)
            value = self._unbox_scalar(value)
        elif is_valid_nat_for_dtype(value, self.dtype):
            value = iNaT
        elif not isna(value) and lib.is_integer(value) and value == iNaT:
            # exclude misc e.g. object() and any NAs not allowed above
            value = iNaT
        else:
            msg = (
                "'value' should be a '{scalar}', 'NaT', or array of those. "
                "Got '{typ}' instead."
            )
            raise TypeError(
                msg.format(scalar=self._scalar_type.__name__, typ=type(value).__name__)
            )
        self._data[key] = value
        self._maybe_clear_freq()
