    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def drop_duplicates(self, keep: str | bool = "first") -> MultiIndex:
        return super().drop_duplicates(keep=keep)
