    def _maybe_box(self, func, dropna=False):
        """
        evaluate a function with possible input/output conversion if we are i8

        Parameters
        ----------
        dropna : bool, default False
           whether to drop values if necessary

        """
        if dropna:
            values = self.dropna().values
        else:
            values = self.values

        if com.needs_i8_conversion(self):
            boxer = com.i8_boxer(self)

            if len(values) == 0:
                return boxer(iNaT)

            values = values.view('i8')
            result = func(values)

            if com.is_list_like(result):
                result = result.map(boxer)
            else:
                result = boxer(result)

        else:

            # let the function return nan if appropriate
            if dropna:
                if len(values) == 0:
                    return np.nan
            result = func(values)

        return result
