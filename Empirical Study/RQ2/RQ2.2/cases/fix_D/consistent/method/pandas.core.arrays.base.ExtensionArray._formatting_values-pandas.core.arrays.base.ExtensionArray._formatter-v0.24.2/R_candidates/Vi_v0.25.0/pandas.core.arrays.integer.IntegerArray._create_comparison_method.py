    @classmethod
    def _create_comparison_method(cls, op):
        def cmp_method(self, other):

            op_name = op.__name__
            mask = None

            if isinstance(other, (ABCSeries, ABCIndexClass)):
                # Rely on pandas to unbox and dispatch to us.
                return NotImplemented

            if isinstance(other, IntegerArray):
                other, mask = other._data, other._mask

            elif is_list_like(other):
                other = np.asarray(other)
                if other.ndim > 0 and len(self) != len(other):
                    raise ValueError("Lengths must match to compare")

            other = lib.item_from_zerodim(other)

            # numpy will show a DeprecationWarning on invalid elementwise
            # comparisons, this will raise in the future
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", "elementwise", FutureWarning)
                with np.errstate(all="ignore"):
                    result = op(self._data, other)

            # nans propagate
            if mask is None:
                mask = self._mask
            else:
                mask = self._mask | mask

            result[mask] = op_name == "ne"
            return result

        name = "__{name}__".format(name=op.__name__)
        return set_function_name(cmp_method, name, cls)
