    def _transform_general(self, func, *args, **kwargs):
        from pandas.core.reshape.concat import concat

        applied = []
        obj = self._obj_with_exclusions
        gen = self.grouper.get_iterator(obj, axis=self.axis)
        fast_path, slow_path = self._define_paths(func, *args, **kwargs)

        # Determine whether to use slow or fast path by evaluating on the first group.
        # Need to handle the case of an empty generator and process the result so that
        # it does not need to be computed again.
        try:
            name, group = next(gen)
        except StopIteration:
            pass
        else:
            object.__setattr__(group, "name", name)
            try:
                path, res = self._choose_path(fast_path, slow_path, group)
            except TypeError:
                return self._transform_item_by_item(obj, fast_path)
            except ValueError as err:
                msg = "transform must return a scalar value for each group"
                raise ValueError(msg) from err
            if group.size > 0:
                res = _wrap_transform_general_frame(self.obj, group, res)
                applied.append(res)

        # Compute and process with the remaining groups
        emit_alignment_warning = False
        for name, group in gen:
            if group.size == 0:
                continue
            object.__setattr__(group, "name", name)
            res = path(group)
            if (
                not emit_alignment_warning
                and res.ndim == 2
                and not res.index.equals(group.index)
            ):
                emit_alignment_warning = True

            res = _wrap_transform_general_frame(self.obj, group, res)
            applied.append(res)

        if emit_alignment_warning:
            # GH#45648
            warnings.warn(
                "In a future version of pandas, returning a DataFrame in "
                "groupby.transform will align with the input's index. Apply "
                "`.to_numpy()` to the result in the transform function to keep "
                "the current behavior and silence this warning.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )

        concat_index = obj.columns if self.axis == 0 else obj.index
        other_axis = 1 if self.axis == 0 else 0  # switches between 0 & 1
        concatenated = concat(applied, axis=self.axis, verify_integrity=False)
        concatenated = concatenated.reindex(concat_index, axis=other_axis, copy=False)
        return self._set_result_index_ordered(concatenated)
