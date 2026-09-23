    @cache_readonly
    def result_index(self):
        recons = self.get_group_levels()
        return MultiIndex.from_arrays(recons, names=self.names)
