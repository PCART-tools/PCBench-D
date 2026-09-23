    def to_values(self):
        """
        Return the values of the matrix as a sequence (a,b,c,d,e,f)
        """
        mtx = self.get_matrix()
        return tuple(mtx[:2].swapaxes(0, 1).flatten())
