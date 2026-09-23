    @cache_readonly
    def _ascending_count(self) -> np.ndarray:
        if TYPE_CHECKING:
            groupby_self = cast(groupby.GroupBy, self)
        else:
            groupby_self = self

        return groupby_self._cumcount_array()
