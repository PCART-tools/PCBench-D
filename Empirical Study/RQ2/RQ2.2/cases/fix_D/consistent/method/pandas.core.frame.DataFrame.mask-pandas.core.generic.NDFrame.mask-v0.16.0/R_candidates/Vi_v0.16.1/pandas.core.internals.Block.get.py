    def get(self, item):
        loc = self.items.get_loc(item)
        return self.values[loc]
