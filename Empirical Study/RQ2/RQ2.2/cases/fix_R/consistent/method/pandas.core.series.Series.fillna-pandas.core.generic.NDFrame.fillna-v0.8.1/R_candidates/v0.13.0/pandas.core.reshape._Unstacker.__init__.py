    def __init__(self, values, index, level=-1, value_columns=None):
        if values.ndim == 1:
            values = values[:, np.newaxis]
        self.values = values
        self.value_columns = value_columns

        if value_columns is None and values.shape[1] != 1:  # pragma: no cover
            raise ValueError('must pass column labels for multi-column data')

        self.index = index
        self.level = self.index._get_level_number(level)

        levels = index.levels
        labels = index.labels

        def _make_index(lev, lab):
            i = lev.__class__(_make_index_array_level(lev.values, lab))
            i.name = lev.name
            return i

        self.new_index_levels = [_make_index(lev, lab)
                                 for lev, lab in zip(levels, labels)]
        self.new_index_names = list(index.names)

        self.removed_name = self.new_index_names.pop(self.level)
        self.removed_level = self.new_index_levels.pop(self.level)

        self._make_sorted_values_labels()
        self._make_selectors()
