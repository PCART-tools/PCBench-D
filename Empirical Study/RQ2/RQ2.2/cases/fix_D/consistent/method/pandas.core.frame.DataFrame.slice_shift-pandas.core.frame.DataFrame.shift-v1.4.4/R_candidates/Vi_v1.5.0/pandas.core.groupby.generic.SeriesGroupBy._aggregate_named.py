    def _aggregate_named(self, func, *args, **kwargs):
        # Note: this is very similar to _aggregate_series_pure_python,
        #  but that does not pin group.name
        result = {}
        initialized = False

        for name, group in self:
            object.__setattr__(group, "name", name)

            output = func(group, *args, **kwargs)
            output = libreduction.extract_result(output)
            if not initialized:
                # We only do this validation on the first iteration
                libreduction.check_result_array(output, group.dtype)
                initialized = True
            result[name] = output

        return result
