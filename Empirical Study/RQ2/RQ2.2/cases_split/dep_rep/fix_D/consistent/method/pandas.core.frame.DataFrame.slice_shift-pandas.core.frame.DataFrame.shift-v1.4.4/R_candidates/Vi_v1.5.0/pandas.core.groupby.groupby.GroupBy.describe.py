    @doc(DataFrame.describe)
    def describe(self, **kwargs):
        with self._group_selection_context():
            if len(self._selected_obj) == 0:
                described = self._selected_obj.describe(**kwargs)
                if self._selected_obj.ndim == 1:
                    result = described
                else:
                    result = described.unstack()
                return result.to_frame().T.iloc[:0]

            result = self._python_apply_general(
                lambda x: x.describe(**kwargs),
                self._selected_obj,
                not_indexed_same=True,
            )
            if self.axis == 1:
                return result.T
            return result.unstack()
