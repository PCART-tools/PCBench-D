    @classmethod
    def _create_comparison_method(cls, op):
        def cmp_method(self, other):
            from pandas.arrays import IntegerArray

            if isinstance(
                other, (ABCDataFrame, ABCSeries, ABCIndexClass, IntegerArray)
            ):
                # Rely on pandas to unbox and dispatch to us.
                return NotImplemented

            other = lib.item_from_zerodim(other)
            mask = None

            if isinstance(other, BooleanArray):
                other, mask = other._data, other._mask

            elif is_list_like(other):
                other = np.asarray(other)
                if other.ndim > 1:
                    raise NotImplementedError(
                        "can only perform ops with 1-d structures"
                    )
                if len(self) != len(other):
                    raise ValueError("Lengths must match to compare")

            if other is libmissing.NA:
                # numpy does not handle pd.NA well as "other" scalar (it returns
                # a scalar False instead of an array)
                result = np.zeros_like(self._data)
                mask = np.ones_like(self._data)
            else:
                # numpy will show a DeprecationWarning on invalid elementwise
                # comparisons, this will raise in the future
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", "elementwise", FutureWarning)
                    with np.errstate(all="ignore"):
                        result = op(self._data, other)

                # nans propagate
                if mask is None:
                    mask = self._mask.copy()
                else:
                    mask = self._mask | mask

            return BooleanArray(result, mask, copy=False)

        name = f"__{op.__name__}"
        return set_function_name(cmp_method, name, cls)
