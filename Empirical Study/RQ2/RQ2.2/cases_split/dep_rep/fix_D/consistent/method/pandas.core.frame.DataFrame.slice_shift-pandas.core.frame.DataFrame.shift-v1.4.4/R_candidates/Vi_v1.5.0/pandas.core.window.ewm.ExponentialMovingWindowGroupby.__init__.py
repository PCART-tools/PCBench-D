    def __init__(self, obj, *args, _grouper=None, **kwargs) -> None:
        super().__init__(obj, *args, _grouper=_grouper, **kwargs)

        if not obj.empty and self.times is not None:
            # sort the times and recalculate the deltas according to the groups
            groupby_order = np.concatenate(list(self._grouper.indices.values()))
            self._deltas = _calculate_deltas(
                self.times.take(groupby_order),  # type: ignore[union-attr]
                self.halflife,
            )
