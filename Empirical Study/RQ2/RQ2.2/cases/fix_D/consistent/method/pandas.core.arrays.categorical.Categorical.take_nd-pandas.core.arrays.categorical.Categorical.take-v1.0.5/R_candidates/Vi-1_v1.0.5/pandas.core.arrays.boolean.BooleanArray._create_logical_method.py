    @classmethod
    def _create_logical_method(cls, op):
        def logical_method(self, other):
            if isinstance(other, (ABCDataFrame, ABCSeries, ABCIndexClass)):
                # Rely on pandas to unbox and dispatch to us.
                return NotImplemented

            assert op.__name__ in {"or_", "ror_", "and_", "rand_", "xor", "rxor"}
            other = lib.item_from_zerodim(other)
            other_is_booleanarray = isinstance(other, BooleanArray)
            other_is_scalar = lib.is_scalar(other)
            mask = None

            if other_is_booleanarray:
                other, mask = other._data, other._mask
            elif is_list_like(other):
                other = np.asarray(other, dtype="bool")
                if other.ndim > 1:
                    raise NotImplementedError(
                        "can only perform ops with 1-d structures"
                    )
                other, mask = coerce_to_array(other, copy=False)
            elif isinstance(other, np.bool_):
                other = other.item()

            if other_is_scalar and not (other is libmissing.NA or lib.is_bool(other)):
                raise TypeError(
                    "'other' should be pandas.NA or a bool. "
                    f"Got {type(other).__name__} instead."
                )

            if not other_is_scalar and len(self) != len(other):
                raise ValueError("Lengths must match to compare")

            if op.__name__ in {"or_", "ror_"}:
                result, mask = ops.kleene_or(self._data, other, self._mask, mask)
            elif op.__name__ in {"and_", "rand_"}:
                result, mask = ops.kleene_and(self._data, other, self._mask, mask)
            elif op.__name__ in {"xor", "rxor"}:
                result, mask = ops.kleene_xor(self._data, other, self._mask, mask)

            return BooleanArray(result, mask)

        name = f"__{op.__name__}__"
        return set_function_name(logical_method, name, cls)
