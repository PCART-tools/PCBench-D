    @Substitution(name="window", versionadded="\n.. versionadded:: 1.0.0\n")
    @Appender(_shared_docs["var"])
    def var(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("var", args, kwargs)
        window_func = partial(self._get_roll_func("roll_weighted_var"), ddof=ddof)
        window_func = get_weighted_roll_func(window_func)
        kwargs.pop("name", None)
        return self._apply(
            window_func, center=self.center, is_weighted=True, name="var", **kwargs
        )
