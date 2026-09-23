    def _get_index_label_from_obj(self) -> Sequence[Hashable]:
        if isinstance(self.obj.index, ABCMultiIndex):
            return self._get_index_label_multiindex()
        else:
            return self._get_index_label_flat()
