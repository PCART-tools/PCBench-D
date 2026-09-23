    def replace(self: T, to_replace, value, inplace: bool) -> T:
        inplace = validate_bool_kwarg(inplace, "inplace")
        assert np.ndim(value) == 0, value
        # TODO "replace" is right now implemented on the blocks, we should move
        # it to general array algos so it can be reused here
        return self.apply_with_block(
            "replace", value=value, to_replace=to_replace, inplace=inplace
        )
