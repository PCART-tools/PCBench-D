    def _verify_integrity(self) -> None:
        n_rows, n_columns = self.shape_proper
        if not len(self.arrays) == n_columns:
            raise ValueError(
                "Number of passed arrays must equal the size of the column Index: "
                f"{len(self.arrays)} arrays vs {n_columns} columns."
            )
        for arr in self.arrays:
            if not len(arr) == n_rows:
                raise ValueError(
                    "Passed arrays should have the same length as the rows Index: "
                    f"{len(arr)} vs {n_rows} rows"
                )
            if not isinstance(arr, (np.ndarray, ExtensionArray)):
                raise ValueError(
                    "Passed arrays should be np.ndarray or ExtensionArray instances, "
                    f"got {type(arr)} instead"
                )
            if not arr.ndim == 1:
                raise ValueError(
                    "Passed arrays should be 1-dimensional, got array with "
                    f"{arr.ndim} dimensions instead."
                )
