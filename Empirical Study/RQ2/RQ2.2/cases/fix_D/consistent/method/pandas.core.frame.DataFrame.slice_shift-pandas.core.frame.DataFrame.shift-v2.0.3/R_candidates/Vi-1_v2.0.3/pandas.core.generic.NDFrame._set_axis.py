    @final
    def _set_axis(self, axis: AxisInt, labels: AnyArrayLike | list) -> None:
        """
        This is called from the cython code when we set the `index` attribute
        directly, e.g. `series.index = [1, 2, 3]`.
        """
        labels = ensure_index(labels)
        self._mgr.set_axis(axis, labels)
        self._clear_item_cache()
