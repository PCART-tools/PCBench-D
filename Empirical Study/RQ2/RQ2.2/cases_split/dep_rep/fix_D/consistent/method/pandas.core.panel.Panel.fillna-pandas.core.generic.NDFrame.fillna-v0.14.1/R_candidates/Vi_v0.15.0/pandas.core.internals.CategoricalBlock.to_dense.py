    def to_dense(self):
        return self.values.to_dense().view()
