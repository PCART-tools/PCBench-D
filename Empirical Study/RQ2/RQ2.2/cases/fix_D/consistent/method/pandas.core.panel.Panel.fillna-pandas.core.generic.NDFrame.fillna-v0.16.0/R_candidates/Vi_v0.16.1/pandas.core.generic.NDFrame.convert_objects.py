    def convert_objects(self, convert_dates=True, convert_numeric=False,
                        convert_timedeltas=True, copy=True):
        """
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

        Returns
        -------
        converted : same as input object
        """
        return self._constructor(
            self._data.convert(convert_dates=convert_dates,
                               convert_numeric=convert_numeric,
                               convert_timedeltas=convert_timedeltas,
                               copy=copy)).__finalize__(self)
