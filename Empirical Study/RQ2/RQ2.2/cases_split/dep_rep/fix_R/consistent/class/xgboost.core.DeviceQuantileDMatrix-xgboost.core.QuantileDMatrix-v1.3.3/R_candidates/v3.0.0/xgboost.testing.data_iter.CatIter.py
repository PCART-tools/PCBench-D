class CatIter(DataIter):  # pylint: disable=too-many-instance-attributes
    """An iterator for testing categorical features."""

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        n_samples_per_batch: int,
        n_features: int,
        *,
        n_batches: int,
        n_cats: int,
        sparsity: float,
        cat_ratio: float,
        onehot: bool,
        device: str,
        cache: Optional[str],
    ) -> None:
        super().__init__(cache_prefix=cache)
        self.n_batches = n_batches
        self.device = device

        n_samples = n_samples_per_batch * n_batches
        cat, y = tm.make_categorical(
            n_samples,
            n_features,
            n_categories=n_cats,
            onehot=onehot,
            cat_ratio=cat_ratio,
            sparsity=sparsity,
        )
        xs, ys = [], []

        prev = 0
        for _ in range(n_batches):
            n = min(n_samples_per_batch, n_samples - prev)
            X = cat.iloc[prev : prev + n, :]
            xs.append(X)
            ys.append(y[prev : prev + n])
            prev += n_samples_per_batch

        self.xs = xs
        self.ys = ys

        self.x = cat
        self.y = y

        self._it = 0

    def xy(self) -> tuple:
        """Return the concatenated data."""
        return self.x, self.y

    def next(self, input_data: Callable) -> bool:
        if self._it == self.n_batches:
            return False

        X, y = self.xs[self._it], self.ys[self._it]
        if self.device == "cuda":
            import cudf
            import cupy

            X = cudf.DataFrame(X)
            y = cupy.array(y)
        input_data(data=X, label=y)
        self._it += 1
        return True

    def reset(self) -> None:
        self._it = 0
