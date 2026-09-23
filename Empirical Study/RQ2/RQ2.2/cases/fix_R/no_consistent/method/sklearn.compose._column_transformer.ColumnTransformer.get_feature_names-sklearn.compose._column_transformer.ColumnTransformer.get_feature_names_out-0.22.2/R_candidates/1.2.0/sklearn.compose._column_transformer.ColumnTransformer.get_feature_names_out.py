    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input features.

            - If `input_features` is `None`, then `feature_names_in_` is
              used as feature names in. If `feature_names_in_` is not defined,
              then the following input feature names are generated:
              `["x0", "x1", ..., "x(n_features_in_ - 1)"]`.
            - If `input_features` is an array-like, then `input_features` must
              match `feature_names_in_` if `feature_names_in_` is defined.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        check_is_fitted(self)
        input_features = _check_feature_names_in(self, input_features)

        # List of tuples (name, feature_names_out)
        transformer_with_feature_names_out = []
        for name, trans, column, _ in self._iter(fitted=True):
            feature_names_out = self._get_feature_name_out_for_transformer(
                name, trans, column, input_features
            )
            if feature_names_out is None:
                continue
            transformer_with_feature_names_out.append((name, feature_names_out))

        if not transformer_with_feature_names_out:
            # No feature names
            return np.array([], dtype=object)

        return self._add_prefix_for_feature_names_out(
            transformer_with_feature_names_out
        )
