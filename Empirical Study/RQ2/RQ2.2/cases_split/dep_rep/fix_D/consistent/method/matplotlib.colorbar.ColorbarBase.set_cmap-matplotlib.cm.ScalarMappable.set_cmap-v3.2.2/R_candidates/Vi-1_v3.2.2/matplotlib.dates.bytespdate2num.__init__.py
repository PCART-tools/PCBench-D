    def __init__(self, fmt, encoding='utf-8'):
        """
        Parameters
        ----------
        fmt : any valid strptime format
        encoding : str
            Encoding to use on byte input.
        """
        super().__init__(fmt)
        self.encoding = encoding
