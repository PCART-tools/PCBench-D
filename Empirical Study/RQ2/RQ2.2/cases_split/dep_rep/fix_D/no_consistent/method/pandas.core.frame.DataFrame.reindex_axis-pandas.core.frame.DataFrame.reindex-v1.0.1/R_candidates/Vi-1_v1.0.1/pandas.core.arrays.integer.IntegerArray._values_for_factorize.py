    def _values_for_factorize(self) -> Tuple[np.ndarray, Any]:
        # TODO: https://github.com/pandas-dev/pandas/issues/30037
        # use masked algorithms, rather than object-dtype / np.nan.
        return self.to_numpy(na_value=np.nan), np.nan
