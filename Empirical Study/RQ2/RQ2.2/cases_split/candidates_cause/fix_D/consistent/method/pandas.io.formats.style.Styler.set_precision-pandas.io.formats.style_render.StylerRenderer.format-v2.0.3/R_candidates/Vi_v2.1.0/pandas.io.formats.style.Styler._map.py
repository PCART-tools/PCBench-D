    def _map(self, func: Callable, subset: Subset | None = None, **kwargs) -> Styler:
        func = partial(func, **kwargs)  # map doesn't take kwargs?
        if subset is None:
            subset = IndexSlice[:]
        subset = non_reducing_slice(subset)
        result = self.data.loc[subset].map(func)
        self._update_ctx(result)
        return self
