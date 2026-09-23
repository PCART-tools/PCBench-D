    def convert_objects(self, convert_dates=True, convert_numeric=False,
                        convert_timedeltas=True, copy=True):
        """
        Deprecated.
        Attempt to infer better dtype for object columns

        Parameters
        ----------
        convert_dates : boolean, default True
            If True, convert to date where possible. If 'coerce', force
            conversion, with unconvertible values becoming NaT.
        convert_numeric : boolean, default False
            If True, attempt to coerce to numbers (including strings), with
            unconvertible values becoming NaN.
        convert_timedeltas : boolean, default True
            If True, convert to timedelta where possible. If 'coerce', force
            conversion, with unconvertible values becoming NaT.
        copy : boolean, default True
            If True, return a copy even if no copy is necessary (e.g. no
            conversion was done). Note: This is meant for internal use, and
            should not be confused with inplace.

        See Also
        --------
        pandas.to_datetime : Convert argument to datetime.
        pandas.to_timedelta : Convert argument to timedelta.
        pandas.to_numeric : Return a fixed frequency timedelta index,
            with day as the default.

        Returns
        -------
        converted : same as input object
        """
        msg = ("convert_objects is deprecated.  To re-infer data dtypes for "
               "object columns, use {klass}.infer_objects()\nFor all "
               "other conversions use the data-type specific converters "
               "pd.to_datetime, pd.to_timedelta and pd.to_numeric."
               ).format(klass=self.__class__.__name__)
        warnings.warn(msg, FutureWarning, stacklevel=2)

        return self._constructor(
            self._data.convert(convert_dates=convert_dates,
                               convert_numeric=convert_numeric,
                               convert_timedeltas=convert_timedeltas,
                               copy=copy)).__finalize__(self)
