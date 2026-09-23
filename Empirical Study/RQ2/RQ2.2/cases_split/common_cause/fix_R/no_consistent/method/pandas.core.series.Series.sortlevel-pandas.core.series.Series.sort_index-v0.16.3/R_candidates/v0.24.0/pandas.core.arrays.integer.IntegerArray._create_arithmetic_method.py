    @classmethod
    def _create_arithmetic_method(cls, op):
        def integer_arithmetic_method(self, other):

            op_name = op.__name__
            mask = None

            if isinstance(other, (ABCSeries, ABCIndexClass)):
                # Rely on pandas to unbox and dispatch to us.
                return NotImplemented

            if getattr(other, 'ndim', 0) > 1:
                raise NotImplementedError(
                    "can only perform ops with 1-d structures")

            if isinstance(other, IntegerArray):
                other, mask = other._data, other._mask

            elif getattr(other, 'ndim', None) == 0:
                other = other.item()

            elif is_list_like(other):
                other = np.asarray(other)
                if not other.ndim:
                    other = other.item()
                elif other.ndim == 1:
                    if not (is_float_dtype(other) or is_integer_dtype(other)):
                        raise TypeError(
                            "can only perform ops with numeric values")
            else:
                if not (is_float(other) or is_integer(other)):
                    raise TypeError("can only perform ops with numeric values")

            # nans propagate
            if mask is None:
                mask = self._mask
            else:
                mask = self._mask | mask

            # 1 ** np.nan is 1. So we have to unmask those.
            if op_name == 'pow':
                mask = np.where(self == 1, False, mask)

            elif op_name == 'rpow':
                mask = np.where(other == 1, False, mask)

            with np.errstate(all='ignore'):
                result = op(self._data, other)

            # divmod returns a tuple
            if op_name == 'divmod':
                div, mod = result
                return (self._maybe_mask_result(div, mask, other, 'floordiv'),
                        self._maybe_mask_result(mod, mask, other, 'mod'))

            return self._maybe_mask_result(result, mask, other, op_name)

        name = '__{name}__'.format(name=op.__name__)
        return set_function_name(integer_arithmetic_method, name, cls)
