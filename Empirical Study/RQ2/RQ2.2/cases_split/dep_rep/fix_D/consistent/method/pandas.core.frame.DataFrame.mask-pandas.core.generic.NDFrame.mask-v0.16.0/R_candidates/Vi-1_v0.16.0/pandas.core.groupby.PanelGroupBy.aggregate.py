    def aggregate(self, arg, *args, **kwargs):
        """
        Aggregate using input function or dict of {column -> function}

        Parameters
        ----------
        arg : function or dict
            Function to use for aggregating groups. If a function, must either
            work when passed a Panel or when passed to Panel.apply. If
            pass a dict, the keys must be DataFrame column names

        Returns
        -------
        aggregated : Panel
        """
        if isinstance(arg, compat.string_types):
            return getattr(self, arg)(*args, **kwargs)

        return self._aggregate_generic(arg, *args, **kwargs)
