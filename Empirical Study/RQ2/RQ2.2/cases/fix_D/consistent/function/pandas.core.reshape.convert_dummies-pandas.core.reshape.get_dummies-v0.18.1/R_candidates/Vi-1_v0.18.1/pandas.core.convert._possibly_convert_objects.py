def _possibly_convert_objects(values, convert_dates=True, convert_numeric=True,
                              convert_timedeltas=True, copy=True):
    """ if we have an object dtype, try to coerce dates and/or numbers """

    # if we have passed in a list or scalar
    if isinstance(values, (list, tuple)):
        values = np.array(values, dtype=np.object_)
    if not hasattr(values, 'dtype'):
        values = np.array([values], dtype=np.object_)

    # convert dates
    if convert_dates and values.dtype == np.object_:

        # we take an aggressive stance and convert to datetime64[ns]
        if convert_dates == 'coerce':
            new_values = _possibly_cast_to_datetime(values, 'M8[ns]',
                                                    errors='coerce')

            # if we are all nans then leave me alone
            if not isnull(new_values).all():
                values = new_values

        else:
            values = lib.maybe_convert_objects(values,
                                               convert_datetime=convert_dates)

    # convert timedeltas
    if convert_timedeltas and values.dtype == np.object_:

        if convert_timedeltas == 'coerce':
            from pandas.tseries.timedeltas import to_timedelta
            new_values = to_timedelta(values, coerce=True)

            # if we are all nans then leave me alone
            if not isnull(new_values).all():
                values = new_values

        else:
            values = lib.maybe_convert_objects(
                values, convert_timedelta=convert_timedeltas)

    # convert to numeric
    if values.dtype == np.object_:
        if convert_numeric:
            try:
                new_values = lib.maybe_convert_numeric(values, set(),
                                                       coerce_numeric=True)

                # if we are all nans then leave me alone
                if not isnull(new_values).all():
                    values = new_values

            except:
                pass
        else:
            # soft-conversion
            values = lib.maybe_convert_objects(values)

    values = values.copy() if copy else values

    return values
