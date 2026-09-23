class TestDataset:
    """Contains a dataset in numpy format as well as the relevant objective and metric."""

    def __init__(
        self, name: str, get_dataset: Callable, objective: str, metric: str
    ) -> None:
        self.name = name
        self.objective = objective
        self.metric = metric
        self.X, self.y = get_dataset()
        self.w: Optional[np.ndarray] = None
        self.margin: Optional[np.ndarray] = None

    def set_params(self, params_in: Dict[str, Any]) -> Dict[str, Any]:
        params_in["objective"] = self.objective
        params_in["eval_metric"] = self.metric
        if self.objective == "multi:softmax":
            params_in["num_class"] = int(np.max(self.y) + 1)
        return params_in

    def get_dmat(self) -> xgb.DMatrix:
        return xgb.DMatrix(
            self.X,
            self.y,
            weight=self.w,
            base_margin=self.margin,
            enable_categorical=True,
        )

    def get_device_dmat(self, max_bin: Optional[int]) -> xgb.QuantileDMatrix:
        import cupy as cp

        w = None if self.w is None else cp.array(self.w)
        X = cp.array(self.X, dtype=np.float32)
        y = cp.array(self.y, dtype=np.float32)
        return xgb.QuantileDMatrix(
            X, y, weight=w, base_margin=self.margin, max_bin=max_bin
        )

    def get_external_dmat(self) -> xgb.DMatrix:
        n_samples = self.X.shape[0]
        n_batches = 10
        per_batch = n_samples // n_batches + 1

        predictor = []
        response = []
        weight = []
        for i in range(n_batches):
            beg = i * per_batch
            end = min((i + 1) * per_batch, n_samples)
            assert end != beg
            X = self.X[beg:end, ...]
            y = self.y[beg:end]
            w = self.w[beg:end] if self.w is not None else None
            predictor.append(X)
            response.append(y)
            if w is not None:
                weight.append(w)

        it = IteratorForTest(
            predictor,
            response,
            weight if weight else None,
            cache="cache",
            on_host=False,
        )
        return xgb.DMatrix(it)

    def __repr__(self) -> str:
        return self.name
