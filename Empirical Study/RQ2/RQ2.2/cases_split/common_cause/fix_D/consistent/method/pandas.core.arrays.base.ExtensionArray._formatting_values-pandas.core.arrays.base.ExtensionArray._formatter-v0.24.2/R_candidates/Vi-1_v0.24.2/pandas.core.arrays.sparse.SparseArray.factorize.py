    def factorize(self, na_sentinel=-1):
        # Currently, ExtensionArray.factorize -> Tuple[ndarray, EA]
        # The sparsity on this is backwards from what Sparse would want. Want
        # ExtensionArray.factorize -> Tuple[EA, EA]
        # Given that we have to return a dense array of labels, why bother
        # implementing an efficient factorize?
        labels, uniques = algos.factorize(np.asarray(self),
                                          na_sentinel=na_sentinel)
        uniques = SparseArray(uniques, dtype=self.dtype)
        return labels, uniques
