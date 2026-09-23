    def __setitem__(
        self,
        key: str | Sequence[int] | Sequence[str] | tuple[Any, str | int],
        value: Any,
    ) -> None:  # pragma: no cover
        # df["foo"] = series
        if isinstance(key, str):
            raise TypeError(
                "'DataFrame' object does not support 'Series' assignment by index. "
                "Use 'DataFrame.with_columns'"
            )

        # df[["C", "D"]]
        elif isinstance(key, list):
            # TODO: Use python sequence constructors
            value = np.array(value)
            if value.ndim != 2:
                raise ValueError("can only set multiple columns with 2D matrix")
            if value.shape[1] != len(key):
                raise ValueError(
                    "matrix columns should be equal to list use to determine column"
                    " names"
                )

            # todo! we can parallelize this by calling from_numpy
            columns = []
            for i, name in enumerate(key):
                columns.append(pli.Series(name, value[:, i]))
            self._df = self.with_columns(columns)._df

        # df[a, b]
        elif isinstance(key, tuple):
            row_selection, col_selection = key

            if (
                isinstance(row_selection, pli.Series) and row_selection.dtype == Boolean
            ) or is_bool_sequence(row_selection):
                raise ValueError(
                    "Not allowed to set 'DataFrame' by boolean mask in the "
                    "row position. Consider using 'DataFrame.with_columns'"
                )

            # get series column selection
            if isinstance(col_selection, str):
                s = self.__getitem__(col_selection)
            elif isinstance(col_selection, int):
                s = self[:, col_selection]
            else:
                raise ValueError(f"column selection not understood: {col_selection}")

            # dispatch to __setitem__ of Series to do modification
            s[row_selection] = value

            # now find the location to place series
            # df[idx]
            if isinstance(col_selection, int):
                self.replace_at_idx(col_selection, s)
            # df["foo"]
            elif isinstance(col_selection, str):
                self.replace(col_selection, s)
        else:
            raise ValueError(
                f"Cannot __setitem__ on DataFrame with key: '{key}' "
                f"of type: '{type(key)}' and value: '{value}' "
                f"of type: '{type(value)}'."
            )
