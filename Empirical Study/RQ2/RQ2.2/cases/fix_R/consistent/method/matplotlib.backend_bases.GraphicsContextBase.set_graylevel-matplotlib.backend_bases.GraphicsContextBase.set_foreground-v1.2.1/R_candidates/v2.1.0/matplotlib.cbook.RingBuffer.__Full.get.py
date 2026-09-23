        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:] + self.data[:self.cur]
