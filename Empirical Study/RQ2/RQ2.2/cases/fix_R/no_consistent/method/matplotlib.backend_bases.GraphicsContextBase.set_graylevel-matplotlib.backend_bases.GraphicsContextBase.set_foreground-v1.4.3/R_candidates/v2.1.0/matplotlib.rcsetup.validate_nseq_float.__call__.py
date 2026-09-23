    def __call__(self, s):
        """return a seq of n floats or raise"""
        if isinstance(s, six.string_types):
            s = [x.strip() for x in s.split(',')]
            err_msg = _str_err_msg
        else:
            err_msg = _seq_err_msg

        if self.n is not None and len(s) != self.n:
            raise ValueError(err_msg.format(n=self.n, num=len(s), s=s))

        try:
            return [float(val)
                    if not self.allow_none or val is not None
                    else val
                    for val in s]
        except ValueError:
            raise ValueError('Could not convert all entries to floats')
