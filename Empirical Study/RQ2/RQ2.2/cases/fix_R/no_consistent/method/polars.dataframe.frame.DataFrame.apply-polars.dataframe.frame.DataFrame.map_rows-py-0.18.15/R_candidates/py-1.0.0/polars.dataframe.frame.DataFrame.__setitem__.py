    def __setitem__(
        self,
        key: str | Sequence[int] | Sequence[str] | tuple[Any, str | int],
        value: Any,
    ) -> None:  # pragma: no cover
        # df["foo"] = series
        if isinstance(key, str):
            msg = (
                "DataFrame object does not support `Series` assignment by index"
                "\n\nUse `DataFrame.with_columns`."
            )
            raise TypeError(msg)

        # df[["C", "D"]]
        elif isinstance(key, list):
            # TODO: Use python sequence constructors
            value = np.array(value)
            if value.ndim != 2:
                msg = "can only set multiple columns with 2D matrix"
                raise ValueError(msg)
            if value.shape[1] != len(key):
                msg = "matrix columns should be equal to list used to determine column names"
                raise ValueError(msg)

            # TODO: we can parallelize this by calling from_numpy
            columns = []
            for i, name in enumerate(key):
                columns.append(pl.Series(name, value[:, i]))
            self._df = self.with_columns(columns)._df

        # df[a, b]
        elif isinstance(key, tuple):
            row_selection, col_selection = key

            if (
                isinstance(row_selection, pl.Series) and row_selection.dtype == Boolean
            ) or is_bool_sequence(row_selection):
                msg = (
                    "not allowed to set DataFrame by boolean mask in the row position"
                    "\n\nConsider using `DataFrame.with_columns`."
                )
                raise TypeError(msg)

            # get series column selection
            if isinstance(col_selection, str):
                s = self.__getitem__(col_selection)
            elif isinstance(col_selection, int):
                s = self[:, col_selection]
            else:
                msg = f"unexpected column selection {col_selection!r}"
                raise TypeError(msg)

            # dispatch to __setitem__ of Series to do modification
            s[row_selection] = value

            # now find the location to place series
            # df[idx]
            if isinstance(col_selection, int):
                self.replace_column(col_selection, s)
            # df["foo"]
            elif isinstance(col_selection, str):
                self._replace(col_selection, s)
        else:
            msg = (
                f"cannot use `__setitem__` on DataFrame"
                f" with key {key!r} of type {type(key).__name__!r}"
                f" and value {value!r} of type {type(value).__name__!r}"
            )
            raise TypeError(msg)
