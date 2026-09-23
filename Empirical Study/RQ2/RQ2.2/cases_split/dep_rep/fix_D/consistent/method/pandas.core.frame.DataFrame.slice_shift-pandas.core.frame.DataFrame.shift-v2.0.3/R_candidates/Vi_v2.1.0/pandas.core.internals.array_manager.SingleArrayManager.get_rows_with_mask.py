    def get_rows_with_mask(self, indexer: npt.NDArray[np.bool_]) -> SingleArrayManager:
        new_array = self.array[indexer]
        new_index = self.index[indexer]
        return type(self)([new_array], [new_index])
