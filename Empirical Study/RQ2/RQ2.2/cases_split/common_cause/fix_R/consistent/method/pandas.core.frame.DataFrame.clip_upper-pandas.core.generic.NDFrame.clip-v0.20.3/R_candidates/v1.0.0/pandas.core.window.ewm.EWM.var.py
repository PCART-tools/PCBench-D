    @Substitution(name="ewm")
    @Appender(_doc_template)
    @Appender(_bias_template)
    def var(self, bias=False, *args, **kwargs):
        """
        Exponential weighted moving variance.
        """
        nv.validate_window_func("var", args, kwargs)

        def f(arg):
            return window_aggregations.ewmcov(
                arg,
                arg,
                self.com,
                int(self.adjust),
                int(self.ignore_na),
                int(self.min_periods),
                int(bias),
            )

        return self._apply(f, **kwargs)
