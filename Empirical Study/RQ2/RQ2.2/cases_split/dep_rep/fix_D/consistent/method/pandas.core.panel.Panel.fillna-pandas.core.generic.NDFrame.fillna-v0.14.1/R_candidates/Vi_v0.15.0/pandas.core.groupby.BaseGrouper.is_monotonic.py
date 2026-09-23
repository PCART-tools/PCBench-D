    @cache_readonly
    def is_monotonic(self):
        # return if my group orderings are monotonic
        return Index(self.group_info[0]).is_monotonic
