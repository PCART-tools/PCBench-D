    def to_json(self, path_or_buf=None, orient=None, date_format='epoch',
                double_precision=10, force_ascii=True, date_unit='ms',
                default_handler=None):
        """
        Convert the object to a JSON string.

        Note NaN's and None will be converted to null and datetime objects
        will be converted to UNIX timestamps.

        Parameters
        ----------
        path_or_buf : the path or buffer to write the result string
            if this is None, return a StringIO of the converted string
        orient : string

            * Series

              - default is 'index'
              - allowed values are: {'split','records','index'}

            * DataFrame

              - default is 'columns'
              - allowed values are:
                {'split','records','index','columns','values'}

            * The format of the JSON string

              - split : dict like
                {index -> [index], columns -> [columns], data -> [values]}
              - records : list like
                [{column -> value}, ... , {column -> value}]
              - index : dict like {index -> {column -> value}}
              - columns : dict like {column -> {index -> value}}
              - values : just the values array

        date_format : {'epoch', 'iso'}
            Type of date conversion. `epoch` = epoch milliseconds,
            `iso`` = ISO8601, default is epoch.
        double_precision : The number of decimal places to use when encoding
            floating point values, default 10.
        force_ascii : force encoded string to be ASCII, default True.
        date_unit : string, default 'ms' (milliseconds)
            The time unit to encode to, governs timestamp and ISO8601
            precision.  One of 's', 'ms', 'us', 'ns' for second, millisecond,
            microsecond, and nanosecond respectively.
        default_handler : callable, default None
            Handler to call if object cannot otherwise be converted to a
            suitable format for JSON. Should receive a single argument which is
            the object to convert and return a serialisable object.

        Returns
        -------
        same type as input object with filtered info axis

        """

        from pandas.io import json
        return json.to_json(
            path_or_buf=path_or_buf,
            obj=self, orient=orient,
            date_format=date_format,
            double_precision=double_precision,
            force_ascii=force_ascii,
            date_unit=date_unit,
            default_handler=default_handler)
