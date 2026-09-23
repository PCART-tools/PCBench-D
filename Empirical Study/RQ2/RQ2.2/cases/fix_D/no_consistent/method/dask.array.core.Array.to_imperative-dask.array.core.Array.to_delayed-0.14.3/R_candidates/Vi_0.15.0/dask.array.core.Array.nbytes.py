    @property
    def nbytes(self):
        """ Number of bytes in array """
        return self.size * self.dtype.itemsize
