    def agg(self) -> DataFrame | Series | None:
        """
        Provide an implementation for the aggregators.

        Returns
        -------
        Result of aggregation, or None if agg cannot be performed by
        this method.
        """
        obj = self.obj
        arg = self.f
        args = self.args
        kwargs = self.kwargs

        if isinstance(arg, str):
            return self.apply_str()

        if is_dict_like(arg):
            return self.agg_dict_like()
        elif is_list_like(arg):
            # we require a list, but not a 'str'
            return self.agg_list_like()

        if callable(arg):
            f = com.get_cython_func(arg)
            if f and not args and not kwargs:
                return getattr(obj, f)()

        # caller can react
        return None
