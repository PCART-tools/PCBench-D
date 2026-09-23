    def abs(self):
        """
        Return an object with absolute value taken. Only applicable to objects
        that are all numeric

        Returns
        -------
        abs: type of caller
        """
        obj = np.abs(self)

        # suprimo numpy 1.6 hacking
        if _np_version_under1p7:
            if self.ndim == 1:
                if obj.dtype == 'm8[us]':
                    obj = obj.astype('m8[ns]')
            elif self.ndim == 2:
                def f(x):
                    if x.dtype == 'm8[us]':
                        x = x.astype('m8[ns]')
                    return x

                if 'm8[us]' in obj.dtypes.values:
                    obj = obj.apply(f)

        return obj
