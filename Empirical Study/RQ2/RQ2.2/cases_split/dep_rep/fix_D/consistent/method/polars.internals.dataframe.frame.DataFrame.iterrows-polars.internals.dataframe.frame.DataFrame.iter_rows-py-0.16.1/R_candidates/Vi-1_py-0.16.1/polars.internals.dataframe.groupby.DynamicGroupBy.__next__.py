    def __next__(self) -> tuple[object, DF] | tuple[tuple[object, ...], DF]:
        if self._current_index >= len(self._group_indices):
            raise StopIteration

        group_name = next(self._group_names)
        group_data = self.df[self._group_indices[self._current_index]]
        self._current_index += 1

        return group_name, group_data
