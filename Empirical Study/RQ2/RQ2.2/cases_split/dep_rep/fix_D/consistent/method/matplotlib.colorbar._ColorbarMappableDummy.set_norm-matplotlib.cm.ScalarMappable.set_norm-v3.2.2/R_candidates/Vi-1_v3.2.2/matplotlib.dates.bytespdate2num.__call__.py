    def __call__(self, b):
        """
        Parameters
        ----------
        b : bytes

        Returns
        -------
        date2num float
        """
        s = b.decode(self.encoding)
        return super().__call__(s)
