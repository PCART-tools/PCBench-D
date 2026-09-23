    class _InvalidCatIter(DataIter):
        def __init__(self) -> None:
            super().__init__(cache_prefix=None)
            self._it = 0

        def next(self, input_data: Callable) -> bool:
            if self._it == 2:
                return False
            X, y = tm.make_categorical(
                64,
                12,
                4,
                onehot=False,
                sparsity=0.5,
                cat_ratio=1.0 if self._it == 0 else 0.5,
            )
            if device == "cuda":
                import cudf
                import cupy

                X = cudf.DataFrame(X)
                y = cupy.array(y)

            input_data(data=X, label=y)
            self._it += 1
            return True

        def reset(self) -> None:
            self._it = 0
