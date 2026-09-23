    def __getitem__(self, item):
        return Quantity(self.magnitude[item], self.units)
