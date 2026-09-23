    def _aggregate_named(self, func, *args, **kwargs):
        result = {}

        for name, group in self:
            group.name = name
            output = func(group, *args, **kwargs)
            if isinstance(output, (Series, np.ndarray)):
                raise Exception('Must produce aggregated value')
            result[name] = self._try_cast(output, group)

        return result
