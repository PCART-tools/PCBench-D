    @property
    def nbytes(self):
        return self.left.nbytes + self.right.nbytes
