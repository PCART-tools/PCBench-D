    def __init__(self, values, nat_rep='NaT', box=False, **kwargs):
        super(Timedelta64Formatter, self).__init__(values, **kwargs)
        self.nat_rep = nat_rep
        self.box = box
