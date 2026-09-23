    @property
    def is_separable(self):
        mtx = self.get_matrix()
        return mtx[0, 1] == mtx[1, 0] == 0.0
