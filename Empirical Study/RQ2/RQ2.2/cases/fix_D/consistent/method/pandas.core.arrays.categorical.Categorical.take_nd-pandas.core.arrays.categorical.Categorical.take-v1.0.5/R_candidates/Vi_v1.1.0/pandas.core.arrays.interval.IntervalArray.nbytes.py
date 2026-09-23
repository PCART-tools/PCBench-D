    @property
    def nbytes(self) -> int:
        return self.left.nbytes + self.right.nbytes
