    def _hash_pandas_object(
        self, *, encoding: str, hash_key: str, categorize: bool
    ) -> npt.NDArray[np.uint64]:
        from pandas.core.util.hashing import hash_array

        values = self._ndarray
        return hash_array(
            values, encoding=encoding, hash_key=hash_key, categorize=categorize
        )
