    def autocorr(self, lag=1):
        """
        Lag-N autocorrelation

        Parameters
        ----------
        lag : int, default 1
            Number of lags to apply before performing autocorrelation.

        Returns
        -------
        autocorr : float
        """
        return self.corr(self.shift(lag))
