
    def convert_objects(self, convert_dates=True, convert_numeric=False):
        """
        Attempt to infer better dtype for object columns
        Always returns a copy (even if no object columns)

        Parameters
        ----------
        convert_dates : if True, attempt to soft convert_dates, if 'coerce', force conversion (and non-convertibles get NaT)
        convert_numeric : if True attempt to coerce to numerbers (including strings), non-convertibles get NaN

        Returns
        -------
        converted : DataFrame
        """
        return self._constructor(self._data.convert(convert_dates=convert_dates, convert_numeric=convert_numeric))
