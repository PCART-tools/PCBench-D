    @final
    def replace_regex(self, **kwargs) -> Self:
        return self.apply_with_block(
            "_replace_regex", **kwargs, using_cow=using_copy_on_write()
        )
