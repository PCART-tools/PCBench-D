    def convert_objects(self, convert_dates=True, convert_numeric=False,
                        copy=True):
        """
        Attempt to infer better dtype for object columns

        Parameters
        ----------
        convert_dates : if True, attempt to soft convert_dates, if 'coerce',
            force conversion (and non-convertibles get NaT)
        convert_numeric : if True attempt to coerce to numbers (including
            strings), non-convertibles get NaN
        copy : Boolean, if True, return copy, default is True

        Returns
        -------
        converted : asm as input object
        """
        return self._constructor(
            self._data.convert(convert_dates=convert_dates,
                               convert_numeric=convert_numeric,
                               copy=copy)).__finalize__(self)
