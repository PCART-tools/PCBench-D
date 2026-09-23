    def _get_index_label_flat(self) -> list[str]:
        index_label = self.obj.index.name
        return [""] if index_label is None else [index_label]
