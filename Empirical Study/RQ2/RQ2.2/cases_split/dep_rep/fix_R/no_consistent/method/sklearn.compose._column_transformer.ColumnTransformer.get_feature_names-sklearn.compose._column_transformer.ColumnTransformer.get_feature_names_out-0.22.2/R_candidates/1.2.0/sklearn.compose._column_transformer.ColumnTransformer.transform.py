    def transform(self, X):
        """Transform X separately by each transformer, concatenate results.

        Parameters
        ----------
        X : {array-like, dataframe} of shape (n_samples, n_features)
            The data to be transformed by subset.

        Returns
        -------
        X_t : {array-like, sparse matrix} of \
                shape (n_samples, sum_n_components)
            Horizontally stacked results of transformers. sum_n_components is the
            sum of n_components (output dimension) over transformers. If
            any result is a sparse matrix, everything will be converted to
            sparse matrices.
        """
        check_is_fitted(self)
        X = _check_X(X)

        fit_dataframe_and_transform_dataframe = hasattr(
            self, "feature_names_in_"
        ) and hasattr(X, "columns")

        if fit_dataframe_and_transform_dataframe:
            named_transformers = self.named_transformers_
            # check that all names seen in fit are in transform, unless
            # they were dropped
            non_dropped_indices = [
                ind
                for name, ind in self._transformer_to_input_indices.items()
                if name in named_transformers
                and isinstance(named_transformers[name], str)
                and named_transformers[name] != "drop"
            ]

            all_indices = set(chain(*non_dropped_indices))
            all_names = set(self.feature_names_in_[ind] for ind in all_indices)

            diff = all_names - set(X.columns)
            if diff:
                raise ValueError(f"columns are missing: {diff}")
        else:
            # ndarray was used for fitting or transforming, thus we only
            # check that n_features_in_ is consistent
            self._check_n_features(X, reset=False)

        Xs = self._fit_transform(
            X,
            None,
            _transform_one,
            fitted=True,
            column_as_strings=fit_dataframe_and_transform_dataframe,
        )
        self._validate_output(Xs)

        if not Xs:
            # All transformers are None
            return np.zeros((X.shape[0], 0))

        return self._hstack(list(Xs))
