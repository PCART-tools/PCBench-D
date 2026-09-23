def _flex_method_SERIES(op, name, str_rep, default_axis=None, fill_zeros=None,
                        **eval_kwargs):
    op_name = name.replace('__', '')
    op_desc = _op_descriptions[op_name]
    if op_desc['reversed']:
        equiv = 'other ' + op_desc['op'] + ' series'
    else:
        equiv = 'series ' + op_desc['op'] + ' other'

    doc = """
    %s of series and other, element-wise (binary operator `%s`).

    Equivalent to ``%s``, but with support to substitute a fill_value for
    missing data in one of the inputs.

    Parameters
    ----------
    other: Series or scalar value
    fill_value : None or float value, default None (NaN)
        Fill missing (NaN) values with this value. If both Series are
        missing, the result will be missing
    level : int or name
        Broadcast across a level, matching Index values on the
        passed MultiIndex level

    Returns
    -------
    result : Series

    See also
    --------
    Series.%s
    """ % (op_desc['desc'], op_name, equiv, op_desc['reverse'])

    @Appender(doc)
    def flex_wrapper(self, other, level=None, fill_value=None, axis=0):
        # validate axis
        self._get_axis_number(axis)
        if isinstance(other, ABCSeries):
            return self._binop(other, op, level=level, fill_value=fill_value)
        elif isinstance(other, (np.ndarray, ABCSeries, list, tuple)):
            if len(other) != len(self):
                raise ValueError('Lengths must be equal')
            return self._binop(self._constructor(other, self.index), op,
                               level=level, fill_value=fill_value)
        else:
            if fill_value is not None:
                self = self.fillna(fill_value)

            return self._constructor(op(self.values, other),
                                     self.index).__finalize__(self)

    flex_wrapper.__name__ = name
    return flex_wrapper
