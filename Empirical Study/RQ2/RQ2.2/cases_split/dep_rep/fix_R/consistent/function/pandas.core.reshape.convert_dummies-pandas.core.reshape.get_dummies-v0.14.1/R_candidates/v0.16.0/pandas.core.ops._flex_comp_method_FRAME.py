def _flex_comp_method_FRAME(op, name, str_rep=None, default_axis='columns',
                            masker=False):

    def na_op(x, y):
        try:
            result = op(x, y)
        except TypeError:
            xrav = x.ravel()
            result = np.empty(x.size, dtype=x.dtype)
            if isinstance(y, (np.ndarray, pd.Series)):
                yrav = y.ravel()
                mask = notnull(xrav) & notnull(yrav)
                result[mask] = op(np.array(list(xrav[mask])),
                                  np.array(list(yrav[mask])))
            else:
                mask = notnull(xrav)
                result[mask] = op(np.array(list(xrav[mask])), y)

            if op == operator.ne:  # pragma: no cover
                np.putmask(result, ~mask, True)
            else:
                np.putmask(result, ~mask, False)
            result = result.reshape(x.shape)

        return result

    @Appender('Wrapper for flexible comparison methods %s' % name)
    def f(self, other, axis=default_axis, level=None):
        if isinstance(other, pd.DataFrame):    # Another DataFrame
            return self._flex_compare_frame(other, na_op, str_rep, level)

        elif isinstance(other, pd.Series):
            return self._combine_series(other, na_op, None, axis, level)

        elif isinstance(other, (list, tuple)):
            if axis is not None and self._get_axis_name(axis) == 'index':
                casted = pd.Series(other, index=self.index)
            else:
                casted = pd.Series(other, index=self.columns)

            return self._combine_series(casted, na_op, None, axis, level)

        elif isinstance(other, np.ndarray):
            if other.ndim == 1:
                if axis is not None and self._get_axis_name(axis) == 'index':
                    casted = pd.Series(other, index=self.index)
                else:
                    casted = pd.Series(other, index=self.columns)

                return self._combine_series(casted, na_op, None, axis, level)

            elif other.ndim == 2:
                casted = pd.DataFrame(other, index=self.index,
                                      columns=self.columns)

                return self._flex_compare_frame(casted, na_op, str_rep, level)

            else:
                raise ValueError("Incompatible argument shape: %s" %
                                 (other.shape, ))

        else:
            return self._combine_const(other, na_op)

    f.__name__ = name

    return f
