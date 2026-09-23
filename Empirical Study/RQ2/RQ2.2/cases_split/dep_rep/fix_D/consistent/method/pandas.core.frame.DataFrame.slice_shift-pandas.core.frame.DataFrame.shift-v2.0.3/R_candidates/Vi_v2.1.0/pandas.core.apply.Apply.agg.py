    def agg(self) -> DataFrame | Series | None:
        """
        Provide an implementation for the aggregators.

        Returns
        -------
        Result of aggregation, or None if agg cannot be performed by
        this method.
        """
        obj = self.obj
        func = self.func
        args = self.args
        kwargs = self.kwargs

        if isinstance(func, str):
            return self.apply_str()

        if is_dict_like(func):
            return self.agg_dict_like()
        elif is_list_like(func):
            # we require a list, but not a 'str'
            return self.agg_list_like()

        if callable(func):
            f = com.get_cython_func(func)
            if f and not args and not kwargs:
                warn_alias_replacement(obj, func, f)
                return getattr(obj, f)()

        # caller can react
        return None
