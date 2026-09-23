    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "names"])
    def set_names(self, names, level=None, inplace: bool = False) -> MultiIndex | None:
        return super().set_names(names=names, level=level, inplace=inplace)
