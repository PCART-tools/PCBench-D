    @Substitution(subset=subset_args)
    def applymap(
        self, func: Callable, subset: Subset | None = None, **kwargs
    ) -> Styler:
        """
        Apply a CSS-styling function elementwise.

        .. deprecated:: 2.1.0

           Styler.applymap has been deprecated. Use Styler.map instead.

        Parameters
        ----------
        func : function
            ``func`` should take a scalar and return a string.
        %(subset)s
        **kwargs : dict
            Pass along to ``func``.

        Returns
        -------
        Styler
        """
        warnings.warn(
            "Styler.applymap has been deprecated. Use Styler.map instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.map(func, subset, **kwargs)
