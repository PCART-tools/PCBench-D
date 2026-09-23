    def zfill(self, width):
        """"
        Filling left side with 0

        Parameters
        ----------
        width : int
            Minimum width of resulting string; additional characters will be filled
            with 0

        Returns
        -------
        filled : array
        """
        result = str_pad(self.series, width, side='left', fillchar='0')
        return self._wrap_result(result)
