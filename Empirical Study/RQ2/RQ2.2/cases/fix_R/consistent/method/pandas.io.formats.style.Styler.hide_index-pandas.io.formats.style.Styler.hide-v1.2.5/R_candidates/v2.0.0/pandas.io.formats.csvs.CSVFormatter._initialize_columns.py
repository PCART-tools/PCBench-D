    def _initialize_columns(self, cols: Sequence[Hashable] | None) -> np.ndarray:
        # validate mi options
        if self.has_mi_columns:
            if cols is not None:
                msg = "cannot specify cols with a MultiIndex on the columns"
                raise TypeError(msg)

        if cols is not None:
            if isinstance(cols, ABCIndex):
                cols = cols._format_native_types(**self._number_format)
            else:
                cols = list(cols)
            self.obj = self.obj.loc[:, cols]

        # update columns to include possible multiplicity of dupes
        # and make sure cols is just a list of labels
        new_cols = self.obj.columns
        return new_cols._format_native_types(**self._number_format)
