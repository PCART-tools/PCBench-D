    def _get_index_label_flat(self) -> Sequence[Hashable]:
        index_label = self.obj.index.name
        return [""] if index_label is None else [index_label]
