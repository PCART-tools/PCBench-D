    def convert_objects(self, convert_dates=True, convert_numeric=False,
                        convert_timedeltas=True, copy=True):
        """
        Attempt to infer better dtype for object columns

        Parameters
        ----------
        convert_dates : if True, attempt to soft convert dates, if 'coerce',
            force conversion (and non-convertibles get NaT)
        convert_numeric : if True attempt to coerce to numbers (including
            strings), non-convertibles get NaN
        convert_timedeltas : if True, attempt to soft convert timedeltas, if 'coerce',
            force conversion (and non-convertibles get NaT)
        copy : Boolean, if True, return copy, default is True

        Returns
        -------
        converted : asm as input object
        """
        return self._constructor(
            self._data.convert(convert_dates=convert_dates,
                               convert_numeric=convert_numeric,
                               convert_timedeltas=convert_timedeltas,
                               copy=copy)).__finalize__(self)
