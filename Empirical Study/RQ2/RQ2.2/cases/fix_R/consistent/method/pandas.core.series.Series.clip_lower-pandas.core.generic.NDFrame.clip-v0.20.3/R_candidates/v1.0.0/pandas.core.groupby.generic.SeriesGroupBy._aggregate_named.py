    def _aggregate_named(self, func, *args, **kwargs):
        result = {}

        for name, group in self:
            group.name = name
            output = func(group, *args, **kwargs)
            if isinstance(output, (Series, Index, np.ndarray)):
                raise ValueError("Must produce aggregated value")
            result[name] = output

        return result
