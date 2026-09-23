    def apply(self, f, data: FrameOrSeries, axis: int = 0):
        mutated = self.mutated
        splitter = self._get_splitter(data, axis=axis)
        group_keys = self._get_group_keys()
        result_values = None

        sdata: FrameOrSeries = splitter._get_sorted_data()
        if sdata.ndim == 2 and np.any(sdata.dtypes.apply(is_extension_array_dtype)):
            # calling splitter.fast_apply will raise TypeError via apply_frame_axis0
            #  if we pass EA instead of ndarray
            #  TODO: can we have a workaround for EAs backed by ndarray?
            pass

        elif (
            com.get_callable_name(f) not in base.plotting_methods
            and isinstance(splitter, FrameSplitter)
            and axis == 0
            # fast_apply/libreduction doesn't allow non-numpy backed indexes
            and not sdata.index._has_complex_internals
        ):
            try:
                result_values, mutated = splitter.fast_apply(f, group_keys)

            except libreduction.InvalidApply as err:
                # This Exception is raised if `f` triggers an exception
                # but it is preferable to raise the exception in Python.
                if "Let this error raise above us" not in str(err):
                    # TODO: can we infer anything about whether this is
                    #  worth-retrying in pure-python?
                    raise

            else:
                # If the fast apply path could be used we can return here.
                # Otherwise we need to fall back to the slow implementation.
                if len(result_values) == len(group_keys):
                    return group_keys, result_values, mutated

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
            group_axes = group.axes
            res = f(group)
            if not _is_indexed_like(res, group_axes):
                mutated = True
            result_values.append(res)

        return group_keys, result_values, mutated
