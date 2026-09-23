class IteratorForTest(xgb.core.DataIter):
    """Iterator for testing streaming DMatrix. (external memory, quantile)"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        X: Sequence,
        y: Sequence,
        w: Optional[Sequence],
        *,
        cache: Optional[str],
        on_host: bool = False,
        min_cache_page_bytes: Optional[int] = None,
    ) -> None:
        assert len(X) == len(y)
        self.X = X
        self.y = y
        self.w = w
        self.it = 0
        super().__init__(
            cache_prefix=cache,
            on_host=on_host,
            min_cache_page_bytes=min_cache_page_bytes,
        )

    def next(self, input_data: Callable) -> bool:
        if self.it == len(self.X):
            return False

        with pytest.raises(TypeError, match="Keyword argument"):
            input_data(self.X[self.it], self.y[self.it], None)

        # Use copy to make sure the iterator doesn't hold a reference to the data.
        input_data(
            data=self.X[self.it].copy(),
            label=self.y[self.it].copy(),
            weight=self.w[self.it].copy() if self.w else None,
        )
        gc.collect()  # clear up the copy, see if XGBoost access freed memory.
        self.it += 1
        return True

    def reset(self) -> None:
        self.it = 0

    def as_arrays(
        self,
    ) -> Tuple[Union[np.ndarray, sparse.csr_matrix], ArrayLike, Optional[ArrayLike]]:
        if isinstance(self.X[0], sparse.csr_matrix):
            X = sparse.vstack(self.X, format="csr")
        else:
            X = np.concatenate(self.X, axis=0)
        y = np.concatenate(self.y, axis=0)
        if self.w:
            w = np.concatenate(self.w, axis=0)
        else:
            w = None
        return X, y, w
