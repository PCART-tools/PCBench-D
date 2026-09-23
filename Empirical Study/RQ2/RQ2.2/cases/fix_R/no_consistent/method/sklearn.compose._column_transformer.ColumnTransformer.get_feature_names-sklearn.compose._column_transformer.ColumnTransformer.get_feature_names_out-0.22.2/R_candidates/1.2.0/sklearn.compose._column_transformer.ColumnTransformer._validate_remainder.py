    def _validate_remainder(self, X):
        """
        Validates ``remainder`` and defines ``_remainder`` targeting
        the remaining columns.
        """
        is_transformer = (
            hasattr(self.remainder, "fit") or hasattr(self.remainder, "fit_transform")
        ) and hasattr(self.remainder, "transform")
        if self.remainder not in ("drop", "passthrough") and not is_transformer:
            raise ValueError(
                "The remainder keyword needs to be one of 'drop', "
                "'passthrough', or estimator. '%s' was passed instead"
                % self.remainder
            )

        self._n_features = X.shape[1]
        cols = set(chain(*self._transformer_to_input_indices.values()))
        remaining = sorted(set(range(self._n_features)) - cols)
        self._remainder = ("remainder", self.remainder, remaining)
        self._transformer_to_input_indices["remainder"] = remaining
