    def replace_regex(self: T, **kwargs) -> T:
        return self.apply_with_block("_replace_regex", **kwargs)
