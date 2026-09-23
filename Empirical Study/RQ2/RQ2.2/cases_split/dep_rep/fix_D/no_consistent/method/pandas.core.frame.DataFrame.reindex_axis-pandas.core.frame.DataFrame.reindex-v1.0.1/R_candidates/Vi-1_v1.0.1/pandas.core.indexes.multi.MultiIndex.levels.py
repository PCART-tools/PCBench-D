    @cache_readonly
    def levels(self):
        # Use cache_readonly to ensure that self.get_locs doesn't repeatedly
        # create new IndexEngine
        # https://github.com/pandas-dev/pandas/issues/31648
        result = [
            x._shallow_copy(name=name) for x, name in zip(self._levels, self._names)
        ]
        for level in result:
            # disallow midx.levels[0].name = "foo"
            level._no_setting_name = True
        return FrozenList(result)
