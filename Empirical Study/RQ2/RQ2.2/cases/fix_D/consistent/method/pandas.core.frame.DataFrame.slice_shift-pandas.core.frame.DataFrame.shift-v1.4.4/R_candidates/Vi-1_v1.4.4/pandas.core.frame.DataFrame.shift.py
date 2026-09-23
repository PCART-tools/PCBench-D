    @doc(NDFrame.shift, klass=_shared_doc_kwargs["klass"])
    def shift(
        self,
        periods=1,
        freq: Frequency | None = None,
        axis: Axis = 0,
        fill_value=lib.no_default,
    ) -> DataFrame:
        axis = self._get_axis_number(axis)

        ncols = len(self.columns)
        if (
            axis == 1
            and periods != 0
            and freq is None
            and fill_value is lib.no_default
            and ncols > 0
        ):
            # We will infer fill_value to match the closest column

            # Use a column that we know is valid for our column's dtype GH#38434
            label = self.columns[0]

            if periods > 0:
                result = self.iloc[:, :-periods]
                for col in range(min(ncols, abs(periods))):
                    # TODO(EA2D): doing this in a loop unnecessary with 2D EAs
                    # Define filler inside loop so we get a copy
                    filler = self.iloc[:, 0].shift(len(self))
                    result.insert(0, label, filler, allow_duplicates=True)
            else:
                result = self.iloc[:, -periods:]
                for col in range(min(ncols, abs(periods))):
                    # Define filler inside loop so we get a copy
                    filler = self.iloc[:, -1].shift(len(self))
                    result.insert(
                        len(result.columns), label, filler, allow_duplicates=True
                    )

            result.columns = self.columns.copy()
            return result

        return super().shift(
            periods=periods, freq=freq, axis=axis, fill_value=fill_value
        )
