    @property
    @cacheit
    def dict(self):
        as_int(self.sides) # Check that self.sides can be converted to an integer
        return super(DieDistribution, self).dict
