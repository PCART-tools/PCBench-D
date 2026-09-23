    def _get_index_label_multiindex(self) -> Sequence[Hashable]:
        return [name or "" for name in self.obj.index.names]
