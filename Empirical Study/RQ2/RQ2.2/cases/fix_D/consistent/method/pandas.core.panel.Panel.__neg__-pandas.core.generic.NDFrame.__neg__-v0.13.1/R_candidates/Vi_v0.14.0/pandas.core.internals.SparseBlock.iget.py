    def iget(self, col):
        if col != 0:
            raise IndexError("SparseBlock only contains one item")
        return self.values
