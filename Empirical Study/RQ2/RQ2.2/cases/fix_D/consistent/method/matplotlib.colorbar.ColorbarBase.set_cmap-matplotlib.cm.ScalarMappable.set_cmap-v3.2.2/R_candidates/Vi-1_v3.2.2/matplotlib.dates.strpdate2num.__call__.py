    def __call__(self, s):
        """
        Parameters
        ----------
        s : str

        Returns
        -------
        date2num float
        """
        return date2num(datetime.datetime(*time.strptime(s, self.fmt)[:6]))
