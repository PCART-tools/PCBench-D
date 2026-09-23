    def _aggregate_named(self, func, *args, **kwargs):
        # Note: this is very similar to _aggregate_series_pure_python,
        #  but that does not pin group.name
        result = {}
        initialized = False

        for name, group in self.grouper.get_iterator(
            self._selected_obj, axis=self.axis
        ):
            # needed for pandas/tests/groupby/test_groupby.py::test_basic_aggregations
            object.__setattr__(group, "name", name)

            output = func(group, *args, **kwargs)
            output = ops.extract_result(output)
            if not initialized:
                # We only do this validation on the first iteration
                ops.check_result_array(output, group.dtype)
                initialized = True
            result[name] = output

        return result
