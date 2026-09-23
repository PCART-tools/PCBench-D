def _arith_method_FRAME(op, name, str_rep=None, default_axis='columns',
                        fill_zeros=None, **eval_kwargs):
    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True, **eval_kwargs)
        except TypeError:
            xrav = x.ravel()
            if isinstance(y, (np.ndarray, ABCSeries)):
                dtype = np.find_common_type([x.dtype, y.dtype], [])
                result = np.empty(x.size, dtype=dtype)
                yrav = y.ravel()
                mask = notnull(xrav) & notnull(yrav)
                xrav = xrav[mask]
                yrav = yrav[mask]
                if np.prod(xrav.shape) and np.prod(yrav.shape):
                    result[mask] = op(xrav, yrav)
            elif hasattr(x, 'size'):
                result = np.empty(x.size, dtype=x.dtype)
                mask = notnull(xrav)
                xrav = xrav[mask]
                if np.prod(xrav.shape):
                    result[mask] = op(xrav, y)
            else:
                raise TypeError("cannot perform operation {op} between "
                                "objects of type {x} and {y}".format(
                                    op=name, x=type(x), y=type(y)))

            result, changed = com._maybe_upcast_putmask(result, ~mask, np.nan)
            result = result.reshape(x.shape)

        result = missing.fill_zeros(result, x, y, name, fill_zeros)

        return result

    if name in _op_descriptions:
        op_name = name.replace('__', '')
        op_desc = _op_descriptions[op_name]
        if op_desc['reversed']:
            equiv = 'other ' + op_desc['op'] + ' dataframe'
        else:
            equiv = 'dataframe ' + op_desc['op'] + ' other'

        doc = """
        %s of dataframe and other, element-wise (binary operator `%s`).

        Equivalent to ``%s``, but with support to substitute a fill_value for
        missing data in one of the inputs.

        Parameters
        ----------
        other : Series, DataFrame, or constant
        axis : {0, 1, 'index', 'columns'}
            For Series input, axis to match Series index on
        fill_value : None or float value, default None
            Fill missing (NaN) values with this value. If both DataFrame
            locations are missing, the result will be missing
        level : int or name
            Broadcast across a level, matching Index values on the
            passed MultiIndex level

        Notes
        -----
        Mismatched indices will be unioned together

        Returns
        -------
        result : DataFrame

        See also
        --------
        DataFrame.%s
        """ % (op_desc['desc'], op_name, equiv, op_desc['reverse'])
    else:
        doc = _arith_doc_FRAME % name

    @Appender(doc)
    def f(self, other, axis=default_axis, level=None, fill_value=None):
        if isinstance(other, pd.DataFrame):  # Another DataFrame
            return self._combine_frame(other, na_op, fill_value, level)
        elif isinstance(other, ABCSeries):
            return self._combine_series(other, na_op, fill_value, axis, level)
        elif isinstance(other, (list, tuple)):
            if axis is not None and self._get_axis_name(axis) == 'index':
                # TODO: Get all of these to use _constructor_sliced
                # casted = self._constructor_sliced(other, index=self.index)
                casted = pd.Series(other, index=self.index)
            else:
                # casted = self._constructor_sliced(other, index=self.columns)
                casted = pd.Series(other, index=self.columns)
            return self._combine_series(casted, na_op, fill_value, axis, level)
        elif isinstance(other, np.ndarray) and other.ndim:  # skips np scalar
            if other.ndim == 1:
                if axis is not None and self._get_axis_name(axis) == 'index':
                    # casted = self._constructor_sliced(other,
                    #                                   index=self.index)
                    casted = pd.Series(other, index=self.index)
                else:
                    # casted = self._constructor_sliced(other,
                    #                                   index=self.columns)
                    casted = pd.Series(other, index=self.columns)
                return self._combine_series(casted, na_op, fill_value, axis,
                                            level)
            elif other.ndim == 2:
                # casted = self._constructor(other, index=self.index,
                #                            columns=self.columns)
                casted = pd.DataFrame(other, index=self.index,
                                      columns=self.columns)
                return self._combine_frame(casted, na_op, fill_value, level)
            else:
                raise ValueError("Incompatible argument shape: %s" %
                                 (other.shape, ))
        else:
            if fill_value is not None:
                self = self.fillna(fill_value)

            return self._combine_const(other, na_op)

    f.__name__ = name

    return f
