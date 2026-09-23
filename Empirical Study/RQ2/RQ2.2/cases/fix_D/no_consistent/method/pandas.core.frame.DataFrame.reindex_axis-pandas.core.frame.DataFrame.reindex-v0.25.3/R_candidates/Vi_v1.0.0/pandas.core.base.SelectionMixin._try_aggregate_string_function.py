    def _try_aggregate_string_function(self, arg: str, *args, **kwargs):
        """
        if arg is a string, then try to operate on it:
        - try to find a function (or attribute) on ourselves
        - try to find a numpy function
        - raise

        """
        assert isinstance(arg, str)

        f = getattr(self, arg, None)
        if f is not None:
            if callable(f):
                return f(*args, **kwargs)

            # people may try to aggregate on a non-callable attribute
            # but don't let them think they can pass args to it
            assert len(args) == 0
            assert len([kwarg for kwarg in kwargs if kwarg not in ["axis"]]) == 0
            return f

        f = getattr(np, arg, None)
        if f is not None:
            if hasattr(self, "__array__"):
                # in particular exclude Window
                return f(self, *args, **kwargs)

        raise AttributeError(
            f"'{arg}' is not a valid function for '{type(self).__name__}' object"
        )
