    @final
    def replace(self, to_replace, value, inplace: bool) -> Self:
        inplace = validate_bool_kwarg(inplace, "inplace")
        # NDFrame.replace ensures the not-is_list_likes here
        assert not lib.is_list_like(to_replace)
        assert not lib.is_list_like(value)
        return self.apply_with_block(
            "replace",
            to_replace=to_replace,
            value=value,
            inplace=inplace,
            using_cow=using_copy_on_write(),
        )
