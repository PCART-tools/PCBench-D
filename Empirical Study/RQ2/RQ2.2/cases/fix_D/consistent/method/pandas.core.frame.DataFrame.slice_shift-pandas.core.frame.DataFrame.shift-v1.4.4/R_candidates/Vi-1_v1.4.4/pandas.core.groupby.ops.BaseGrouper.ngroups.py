    @final
    @cache_readonly
    def ngroups(self) -> int:
        return len(self.result_index)
