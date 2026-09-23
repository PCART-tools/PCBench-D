    def __init__(self, categorical, buf=None, length=True,
                 na_rep='NaN', name=False, footer=True):
        self.categorical = categorical
        self.buf = buf if buf is not None else StringIO(u(""))
        self.name = name
        self.na_rep = na_rep
        self.length = length
        self.footer = footer
