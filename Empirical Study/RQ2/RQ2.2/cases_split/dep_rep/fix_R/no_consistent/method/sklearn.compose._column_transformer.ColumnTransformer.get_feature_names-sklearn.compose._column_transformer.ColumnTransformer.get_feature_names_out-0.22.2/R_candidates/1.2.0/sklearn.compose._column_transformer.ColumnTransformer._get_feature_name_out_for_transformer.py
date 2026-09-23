    def _get_feature_name_out_for_transformer(
        self, name, trans, column, feature_names_in
    ):
        """Gets feature names of transformer.

        Used in conjunction with self._iter(fitted=True) in get_feature_names_out.
        """
        column_indices = self._transformer_to_input_indices[name]
        names = feature_names_in[column_indices]
        if trans == "drop" or _is_empty_column_selection(column):
            return
        elif trans == "passthrough":
            return names

        # An actual transformer
        if not hasattr(trans, "get_feature_names_out"):
            raise AttributeError(
                f"Transformer {name} (type {type(trans).__name__}) does "
                "not provide get_feature_names_out."
            )
        return trans.get_feature_names_out(names)
