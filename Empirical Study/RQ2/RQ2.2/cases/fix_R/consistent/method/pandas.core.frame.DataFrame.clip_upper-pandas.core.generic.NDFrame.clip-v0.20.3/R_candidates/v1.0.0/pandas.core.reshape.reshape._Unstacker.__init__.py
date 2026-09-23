    def __init__(
        self,
        values: np.ndarray,
        index,
        level=-1,
        value_columns=None,
        fill_value=None,
        constructor=None,
    ):

        if values.ndim == 1:
            values = values[:, np.newaxis]
        self.values = values
        self.value_columns = value_columns
        self.fill_value = fill_value

        if constructor is None:
            constructor = DataFrame
        self.constructor = constructor

        if value_columns is None and values.shape[1] != 1:  # pragma: no cover
            raise ValueError("must pass column labels for multi-column data")

        self.index = index.remove_unused_levels()

        self.level = self.index._get_level_number(level)

        # when index includes `nan`, need to lift levels/strides by 1
        self.lift = 1 if -1 in self.index.codes[self.level] else 0

        self.new_index_levels = list(self.index.levels)
        self.new_index_names = list(self.index.names)

        self.removed_name = self.new_index_names.pop(self.level)
        self.removed_level = self.new_index_levels.pop(self.level)
        self.removed_level_full = index.levels[self.level]

        # Bug fix GH 20601
        # If the data frame is too big, the number of unique index combination
        # will cause int32 overflow on windows environments.
        # We want to check and raise an error before this happens
        num_rows = np.max([index_level.size for index_level in self.new_index_levels])
        num_columns = self.removed_level.size

        # GH20601: This forces an overflow if the number of cells is too high.
        num_cells = np.multiply(num_rows, num_columns, dtype=np.int32)

        if num_rows > 0 and num_columns > 0 and num_cells <= 0:
            raise ValueError("Unstacked DataFrame is too big, causing int32 overflow")

        self._make_sorted_values_labels()
        self._make_selectors()
