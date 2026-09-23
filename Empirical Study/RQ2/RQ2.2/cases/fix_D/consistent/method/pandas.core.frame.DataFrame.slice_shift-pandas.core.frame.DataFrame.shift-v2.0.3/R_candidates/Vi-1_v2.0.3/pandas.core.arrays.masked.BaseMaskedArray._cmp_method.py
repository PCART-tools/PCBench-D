    def _cmp_method(self, other, op) -> BooleanArray:
        from pandas.core.arrays import BooleanArray

        mask = None

        if isinstance(other, BaseMaskedArray):
            other, mask = other._data, other._mask

        elif is_list_like(other):
            other = np.asarray(other)
            if other.ndim > 1:
                raise NotImplementedError("can only perform ops with 1-d structures")
            if len(self) != len(other):
                raise ValueError("Lengths must match to compare")

        if other is libmissing.NA:
            # numpy does not handle pd.NA well as "other" scalar (it returns
            # a scalar False instead of an array)
            # This may be fixed by NA.__array_ufunc__. Revisit this check
            # once that's implemented.
            result = np.zeros(self._data.shape, dtype="bool")
            mask = np.ones(self._data.shape, dtype="bool")
        else:
            with warnings.catch_warnings():
                # numpy may show a FutureWarning or DeprecationWarning:
                #     elementwise comparison failed; returning scalar instead,
                #     but in the future will perform elementwise comparison
                # before returning NotImplemented. We fall back to the correct
                # behavior today, so that should be fine to ignore.
                warnings.filterwarnings("ignore", "elementwise", FutureWarning)
                warnings.filterwarnings("ignore", "elementwise", DeprecationWarning)
                with np.errstate(all="ignore"):
                    method = getattr(self._data, f"__{op.__name__}__")
                    result = method(other)

                if result is NotImplemented:
                    result = invalid_comparison(self._data, other, op)

        mask = self._propagate_mask(mask, other)
        return BooleanArray(result, mask, copy=False)
