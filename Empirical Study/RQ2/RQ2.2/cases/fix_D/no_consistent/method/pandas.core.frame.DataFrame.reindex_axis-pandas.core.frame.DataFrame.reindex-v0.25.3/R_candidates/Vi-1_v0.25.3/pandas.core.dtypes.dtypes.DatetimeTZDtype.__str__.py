    def __str__(self):
        return "datetime64[{unit}, {tz}]".format(unit=self.unit, tz=self.tz)
