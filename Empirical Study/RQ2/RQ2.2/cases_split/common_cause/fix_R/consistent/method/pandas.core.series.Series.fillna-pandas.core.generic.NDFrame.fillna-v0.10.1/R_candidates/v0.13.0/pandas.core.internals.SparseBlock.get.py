    def get(self, item):
        if self.ndim == 1:
            loc = self.items.get_loc(item)
            return self.values[loc]
        else:
            return self.values
