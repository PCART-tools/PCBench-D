    @cache_readonly
    def ngroups(self):
        return len(self.result_index)
