    def __call__(self, s):
        """Return a list of *n* ints or raise."""
        if isinstance(s, str):
            s = [x.strip() for x in s.split(',')]
            err_msg = _str_err_msg
        else:
            err_msg = _seq_err_msg

        if self.n is not None and len(s) != self.n:
            raise ValueError(err_msg.format(n=self.n, num=len(s), s=s))

        try:
            return [int(val) for val in s]
        except ValueError:
            raise ValueError('Could not convert all entries to ints')
