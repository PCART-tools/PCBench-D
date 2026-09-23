    def __init__(self, data=None, fill_value=np.nan):

        # see gh-13784
        warnings.warn("SparseList is deprecated and will be removed "
                      "in a future version", FutureWarning, stacklevel=2)

        self.fill_value = fill_value
        self._chunks = []

        if data is not None:
            self.append(data)
