    @property
    def flags(self) -> dict[str, bool]:
        """
        Get flags that are set on the Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.flags
        {'SORTED_ASC': False, 'SORTED_DESC': False}
        """
        out = {
            "SORTED_ASC": self._s.is_sorted_ascending_flag(),
            "SORTED_DESC": self._s.is_sorted_descending_flag(),
        }
        if self.dtype == List:
            out["FAST_EXPLODE"] = self._s.can_fast_explode_flag()
        return out
