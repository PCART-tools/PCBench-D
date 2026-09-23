    def __get_item__(self, i):
        return self.data[i % len(self.data)]
