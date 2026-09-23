    def __init__(self, values, nat_rep='NaT', date_format=None, **kwargs):
        super(Datetime64Formatter, self).__init__(values, **kwargs)
        self.nat_rep = nat_rep
        self.date_format = date_format
