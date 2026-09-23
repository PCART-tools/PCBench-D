    def _convert_to_array(self, values, name=None, other=None):
        """converts values to ndarray"""
        from pandas.tseries.timedeltas import _possibly_cast_to_timedelta

        coerce = 'compat' if pd._np_version_under1p7 else True
        if not is_list_like(values):
            values = np.array([values])
        inferred_type = lib.infer_dtype(values)

        if inferred_type in ('datetime64', 'datetime', 'date', 'time'):
            # if we have a other of timedelta, but use pd.NaT here we
            # we are in the wrong path
            if (other is not None and other.dtype == 'timedelta64[ns]' and
                    all(isnull(v) for v in values)):
                values = np.empty(values.shape, dtype=other.dtype)
                values[:] = tslib.iNaT

            # a datetlike
            elif not (isinstance(values, (pa.Array, pd.Series)) and
                      com.is_datetime64_dtype(values)):
                values = tslib.array_to_datetime(values)
            elif isinstance(values, pd.DatetimeIndex):
                values = values.to_series()
        elif inferred_type in ('timedelta', 'timedelta64'):
            # have a timedelta, convert to to ns here
            values = _possibly_cast_to_timedelta(values, coerce=coerce, dtype='timedelta64[ns]')
        elif inferred_type == 'integer':
            # py3 compat where dtype is 'm' but is an integer
            if values.dtype.kind == 'm':
                values = values.astype('timedelta64[ns]')
            elif isinstance(values, pd.PeriodIndex):
                values = values.to_timestamp().to_series()
            elif name not in ('__truediv__', '__div__', '__mul__'):
                raise TypeError("incompatible type for a datetime/timedelta "
                                "operation [{0}]".format(name))
        elif isinstance(values[0], pd.DateOffset):
            # handle DateOffsets
            os = pa.array([getattr(v, 'delta', None) for v in values])
            mask = isnull(os)
            if mask.any():
                raise TypeError("cannot use a non-absolute DateOffset in "
                                "datetime/timedelta operations [{0}]".format(
                                    ', '.join([com.pprint_thing(v)
                                               for v in values[mask]])))
            values = _possibly_cast_to_timedelta(os, coerce=coerce)
        elif inferred_type == 'floating':

            # all nan, so ok, use the other dtype (e.g. timedelta or datetime)
            if isnull(values).all():
                values = np.empty(values.shape, dtype=other.dtype)
                values[:] = tslib.iNaT
            else:
                raise TypeError(
                    'incompatible type [{0}] for a datetime/timedelta '
                    'operation'.format(pa.array(values).dtype))
        else:
            raise TypeError("incompatible type [{0}] for a datetime/timedelta"
                            " operation".format(pa.array(values).dtype))

        return values
