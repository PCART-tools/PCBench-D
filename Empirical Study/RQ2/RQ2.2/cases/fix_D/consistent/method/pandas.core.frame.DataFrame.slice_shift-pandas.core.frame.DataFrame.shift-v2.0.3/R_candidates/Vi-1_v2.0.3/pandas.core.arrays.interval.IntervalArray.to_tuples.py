    @Appender(
        _interval_shared_docs["to_tuples"] % {"return_type": "ndarray", "examples": ""}
    )
    def to_tuples(self, na_tuple: bool = True) -> np.ndarray:
        tuples = com.asarray_tuplesafe(zip(self._left, self._right))
        if not na_tuple:
            # GH 18756
            tuples = np.where(~self.isna(), tuples, np.nan)
        return tuples
