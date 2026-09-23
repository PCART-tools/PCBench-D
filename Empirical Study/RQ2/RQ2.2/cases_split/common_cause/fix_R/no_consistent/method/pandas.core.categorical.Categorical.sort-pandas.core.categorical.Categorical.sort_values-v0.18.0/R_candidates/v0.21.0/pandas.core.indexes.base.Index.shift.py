    def shift(self, periods=1, freq=None):
        """
        Shift Index containing datetime objects by input number of periods and
        DateOffset

        Returns
        -------
        shifted : Index
        """
        raise NotImplementedError("Not supported for type %s" %
                                  type(self).__name__)
