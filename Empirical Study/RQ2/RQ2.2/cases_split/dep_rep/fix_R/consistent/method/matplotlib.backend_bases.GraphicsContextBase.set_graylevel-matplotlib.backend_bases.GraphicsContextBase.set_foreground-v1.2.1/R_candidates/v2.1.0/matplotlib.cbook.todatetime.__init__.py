    def __init__(self, fmt='%Y-%m-%d', missing='Null', missingval=None):
        'use a :func:`time.strptime` format string for conversion'
        converter.__init__(self, missing, missingval)
        self.fmt = fmt
