    def zfill(self, width):
        """"
        Filling left side of strings in the Series/Index with 0.
        Equivalent to :meth:`str.zfill`.

        Parameters
        ----------
        width : int
            Minimum width of resulting string; additional characters will be
            filled with 0

        Returns
        -------
        filled : Series/Index of objects
        """
        result = str_pad(self.series, width, side='left', fillchar='0')
        return self._wrap_result(result)
