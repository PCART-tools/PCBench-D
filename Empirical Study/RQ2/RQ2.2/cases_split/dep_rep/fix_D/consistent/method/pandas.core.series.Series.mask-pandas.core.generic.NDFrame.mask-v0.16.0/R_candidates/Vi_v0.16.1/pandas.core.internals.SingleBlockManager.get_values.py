    def get_values(self):
        """ return a dense type view """
        return np.array(self._block.to_dense(),copy=False)
