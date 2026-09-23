    @final
    @property
    def ax(self) -> Index:
        index = self._gpr_index
        if index is None:
            raise ValueError("_set_grouper must be called before ax is accessed")
        return index
