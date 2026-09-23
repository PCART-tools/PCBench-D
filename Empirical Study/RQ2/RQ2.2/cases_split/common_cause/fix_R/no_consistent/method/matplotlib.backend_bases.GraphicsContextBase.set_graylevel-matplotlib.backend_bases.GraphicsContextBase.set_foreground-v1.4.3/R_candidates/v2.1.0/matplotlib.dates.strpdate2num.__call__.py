    def __call__(self, s):
        """s : string to be converted
           return value: a date2num float
        """
        return date2num(datetime.datetime(*time.strptime(s, self.fmt)[:6]))
