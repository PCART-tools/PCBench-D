    def __init__(
        self, index: MultiIndex, level: Level, constructor, sort: bool = True
    ) -> None:
        self.constructor = constructor
        self.sort = sort

        self.index = index.remove_unused_levels()

        self.level = self.index._get_level_number(level)

        # when index includes `nan`, need to lift levels/strides by 1
        self.lift = 1 if -1 in self.index.codes[self.level] else 0

        # Note: the "pop" below alters these in-place.
        self.new_index_levels = list(self.index.levels)
        self.new_index_names = list(self.index.names)

        self.removed_name = self.new_index_names.pop(self.level)
        self.removed_level = self.new_index_levels.pop(self.level)
        self.removed_level_full = index.levels[self.level]
        if not self.sort:
            unique_codes = unique(self.index.codes[self.level])
            self.removed_level = self.removed_level.take(unique_codes)
            self.removed_level_full = self.removed_level_full.take(unique_codes)

        # Bug fix GH 20601
        # If the data frame is too big, the number of unique index combination
        # will cause int32 overflow on windows environments.
        # We want to check and raise an warning before this happens
        num_rows = np.max([index_level.size for index_level in self.new_index_levels])
        num_columns = self.removed_level.size

        # GH20601: This forces an overflow if the number of cells is too high.
        num_cells = num_rows * num_columns

        # GH 26314: Previous ValueError raised was too restrictive for many users.
        if num_cells > np.iinfo(np.int32).max:
            warnings.warn(
                f"The following operation may generate {num_cells} cells "
                f"in the resulting pandas object.",
                PerformanceWarning,
                stacklevel=find_stack_level(),
            )

        self._make_selectors()
