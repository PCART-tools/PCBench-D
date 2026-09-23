    @property
    def obj(self) -> NDFrame:  # type: ignore[override]
        # error: Incompatible return value type (got "Optional[Any]",
        # expected "NDFrameT")
        return self.groupby.obj  # type: ignore[return-value]
