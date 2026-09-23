    def _create_data_for_split_and_tight_to_dict(
        self, are_all_object_dtype_cols: bool, object_dtype_indices: list[int]
    ) -> list:
        """
        Simple helper method to create data for to ``to_dict(orient="split")`` and
        ``to_dict(orient="tight")`` to create the main output data
        """
        if are_all_object_dtype_cols:
            data = [
                list(map(maybe_box_native, t))
                for t in self.itertuples(index=False, name=None)
            ]
        else:
            data = [list(t) for t in self.itertuples(index=False, name=None)]
            if object_dtype_indices:
                # If we have object_dtype_cols, apply maybe_box_naive after list
                # comprehension for perf
                for row in data:
                    for i in object_dtype_indices:
                        row[i] = maybe_box_native(row[i])
        return data
