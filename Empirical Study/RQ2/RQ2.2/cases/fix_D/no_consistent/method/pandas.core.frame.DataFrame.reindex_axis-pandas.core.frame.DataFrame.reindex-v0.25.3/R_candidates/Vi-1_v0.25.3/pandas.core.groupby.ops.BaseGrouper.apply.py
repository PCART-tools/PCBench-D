    def apply(self, f, data, axis=0):
        mutated = self.mutated
        splitter = self._get_splitter(data, axis=axis)
        group_keys = self._get_group_keys()
        result_values = None

        # oh boy
        f_name = com.get_callable_name(f)
        if (
            f_name not in base.plotting_methods
            and hasattr(splitter, "fast_apply")
            and axis == 0
        ):
            try:
                result_values, mutated = splitter.fast_apply(f, group_keys)

                # If the fast apply path could be used we can return here.
                # Otherwise we need to fall back to the slow implementation.
                if len(result_values) == len(group_keys):
                    return group_keys, result_values, mutated

            except reduction.InvalidApply:
                # Cannot fast apply on MultiIndex (_has_complex_internals).
                # This Exception is also raised if `f` triggers an exception
                # but it is preferable to raise the exception in Python.
                pass
            except Exception:
                # raise this error to the caller
                pass

        for key, (i, group) in zip(group_keys, splitter):
            object.__setattr__(group, "name", key)

            # result_values is None if fast apply path wasn't taken
            # or fast apply aborted with an unexpected exception.
            # In either case, initialize the result list and perform
            # the slow iteration.
            if result_values is None:
                result_values = []

            # If result_values is not None we're in the case that the
            # fast apply loop was broken prematurely but we have
            # already the result for the first group which we can reuse.
            elif i == 0:
                continue

            # group might be modified
            group_axes = _get_axes(group)
            res = f(group)
            if not _is_indexed_like(res, group_axes):
                mutated = True
            result_values.append(res)

        return group_keys, result_values, mutated
