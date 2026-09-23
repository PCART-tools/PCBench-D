    def abs(self):
        """
        Return an object with absolute value taken. Only applicable to objects
        that are all numeric

        Returns
        -------
        abs: type of caller
        """

        # suprimo numpy 1.6 hacking
        # for timedeltas
        if _np_version_under1p7:

            def _convert_timedeltas(x):
                if x.dtype.kind == 'm':
                    return np.abs(x.view('i8')).astype(x.dtype)
                return np.abs(x)

            if self.ndim == 1:
                return _convert_timedeltas(self)
            elif self.ndim == 2:
                return  self.apply(_convert_timedeltas)

        return np.abs(self)
