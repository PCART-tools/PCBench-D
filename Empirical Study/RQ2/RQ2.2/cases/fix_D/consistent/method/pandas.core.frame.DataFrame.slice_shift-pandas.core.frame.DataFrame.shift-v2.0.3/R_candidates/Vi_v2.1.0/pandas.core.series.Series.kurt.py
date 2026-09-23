    @doc(make_doc("kurt", ndim=1))
    def kurt(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.kurt(self, axis, skipna, numeric_only, **kwargs)
