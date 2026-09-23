    @property
    def name(self):
        return "Sparse[{}, {}]".format(self.subtype.name, self.fill_value)
