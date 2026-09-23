    def _get_index_label_multiindex(self) -> list[str]:
        return [name or "" for name in self.obj.index.names]
