    @doc(Series.nlargest)
    def nlargest(self, n: int = 5, keep: str = "first") -> Series:
        f = partial(Series.nlargest, n=n, keep=keep)
        data = self._obj_with_exclusions
        # Don't change behavior if result index happens to be the same, i.e.
        # already ordered and n >= all group sizes.
        result = self._python_apply_general(f, data, not_indexed_same=True)
        return result
