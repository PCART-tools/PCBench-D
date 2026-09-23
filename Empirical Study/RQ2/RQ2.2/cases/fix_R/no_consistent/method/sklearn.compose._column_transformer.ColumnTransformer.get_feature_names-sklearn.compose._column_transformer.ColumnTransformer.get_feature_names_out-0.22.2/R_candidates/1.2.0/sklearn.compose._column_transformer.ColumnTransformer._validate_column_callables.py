    def _validate_column_callables(self, X):
        """
        Converts callable column specifications.
        """
        all_columns = []
        transformer_to_input_indices = {}
        for name, _, columns in self.transformers:
            if callable(columns):
                columns = columns(X)
            all_columns.append(columns)
            transformer_to_input_indices[name] = _get_column_indices(X, columns)

        self._columns = all_columns
        self._transformer_to_input_indices = transformer_to_input_indices
