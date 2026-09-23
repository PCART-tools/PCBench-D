    def __call__(self, b):
        """
        Args:
            b: byte input to be converted
        Returns:
            A date2num float
        """
        s = b.decode(self.encoding)
        return super(bytespdate2num, self).__call__(s)
