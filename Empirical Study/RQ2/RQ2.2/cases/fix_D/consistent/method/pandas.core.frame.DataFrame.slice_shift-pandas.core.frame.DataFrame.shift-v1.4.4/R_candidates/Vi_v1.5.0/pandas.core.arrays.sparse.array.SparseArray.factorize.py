    def factorize(
        self,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ) -> tuple[np.ndarray, SparseArray]:
        # Currently, ExtensionArray.factorize -> Tuple[ndarray, EA]
        # The sparsity on this is backwards from what Sparse would want. Want
        # ExtensionArray.factorize -> Tuple[EA, EA]
        # Given that we have to return a dense array of codes, why bother
        # implementing an efficient factorize?
        codes, uniques = algos.factorize(
            np.asarray(self), na_sentinel=na_sentinel, use_na_sentinel=use_na_sentinel
        )
        if na_sentinel is lib.no_default:
            na_sentinel = -1
        if use_na_sentinel is lib.no_default or use_na_sentinel:
            codes[codes == -1] = na_sentinel
        uniques_sp = SparseArray(uniques, dtype=self.dtype)
        return codes, uniques_sp
