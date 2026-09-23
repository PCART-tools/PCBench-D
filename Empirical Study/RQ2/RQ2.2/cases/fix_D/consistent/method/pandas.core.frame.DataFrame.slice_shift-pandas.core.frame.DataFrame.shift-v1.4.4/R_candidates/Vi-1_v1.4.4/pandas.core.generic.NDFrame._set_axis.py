    def _set_axis(self, axis: int, labels: Index) -> None:
        labels = ensure_index(labels)
        self._mgr.set_axis(axis, labels)
        self._clear_item_cache()
