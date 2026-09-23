    def _init_matrix(self, data, index, columns, dtype=None):
        """ Init self from ndarray or list of lists """
        data = prep_ndarray(data, copy=False)
        index, columns = self._prep_index(data, index, columns)
        data = {idx: data[:, i] for i, idx in enumerate(columns)}
        return self._init_dict(data, index, columns, dtype)
