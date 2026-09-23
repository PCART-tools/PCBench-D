    @Appender(
        _apply_docs["template"].format(
            input="dataframe", examples=_apply_docs["dataframe_examples"]
        )
    )
    def apply(self, func, *args, **kwargs) -> NDFrameT:
        orig_func = func
        func = com.is_builtin_func(func)
        if orig_func != func:
            alias = com._builtin_table_alias[orig_func]
            warn_alias_replacement(self, orig_func, alias)

        if isinstance(func, str):
            if hasattr(self, func):
                res = getattr(self, func)
                if callable(res):
                    return res(*args, **kwargs)
                elif args or kwargs:
                    raise ValueError(f"Cannot pass arguments to property {func}")
                return res

            else:
                raise TypeError(f"apply func should be callable, not '{func}'")

        elif args or kwargs:
            if callable(func):

                @wraps(func)
                def f(g):
                    return func(g, *args, **kwargs)

            else:
                raise ValueError(
                    "func must be a callable if args or kwargs are supplied"
                )
        else:
            f = func

        # ignore SettingWithCopy here in case the user mutates
        with option_context("mode.chained_assignment", None):
            try:
                result = self._python_apply_general(f, self._selected_obj)
            except TypeError:
                # gh-20949
                # try again, with .apply acting as a filtering
                # operation, by excluding the grouping column
                # This would normally not be triggered
                # except if the udf is trying an operation that
                # fails on *some* columns, e.g. a numeric operation
                # on a string grouper column

                return self._python_apply_general(f, self._obj_with_exclusions)

        return result
