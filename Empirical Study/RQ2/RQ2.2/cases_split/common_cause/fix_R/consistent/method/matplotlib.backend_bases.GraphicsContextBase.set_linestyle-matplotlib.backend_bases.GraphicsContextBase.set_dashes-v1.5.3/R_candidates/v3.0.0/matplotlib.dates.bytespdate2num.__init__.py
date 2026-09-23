    def __init__(self, fmt, encoding='utf-8'):
        """
        Args:
            fmt: any valid strptime format is supported
            encoding: encoding to use on byte input (default: 'utf-8')
        """
        super().__init__(fmt)
        self.encoding = encoding
