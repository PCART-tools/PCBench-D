    @lru_cache()
    def errors(self):
        return list(flatten_errors(self.raw_errors))
