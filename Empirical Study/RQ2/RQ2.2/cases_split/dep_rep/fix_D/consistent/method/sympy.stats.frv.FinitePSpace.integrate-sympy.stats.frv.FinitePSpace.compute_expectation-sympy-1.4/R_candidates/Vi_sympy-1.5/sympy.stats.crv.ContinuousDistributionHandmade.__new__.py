    def __new__(cls, pdf, set=Interval(-oo, oo)):
        return Basic.__new__(cls, pdf, set)
