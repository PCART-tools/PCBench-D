    @cache_readonly
    def is_na_after_size_and_isna_all_deprecation(self) -> bool:
        """
        Will self.is_na be True after values.size == 0 deprecation and isna_all
        deprecation are enforced?
        """
        blk = self.block
        if blk.dtype.kind == "V":
            return True
        return False
