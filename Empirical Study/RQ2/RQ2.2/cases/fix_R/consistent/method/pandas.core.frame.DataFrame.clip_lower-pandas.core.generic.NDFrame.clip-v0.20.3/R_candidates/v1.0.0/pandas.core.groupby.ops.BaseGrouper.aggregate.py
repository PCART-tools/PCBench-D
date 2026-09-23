    def aggregate(
        self, values, how: str, axis: int = 0, min_count: int = -1
    ) -> Tuple[np.ndarray, Optional[List[str]]]:
        return self._cython_operation(
            "aggregate", values, how, axis, min_count=min_count
        )
