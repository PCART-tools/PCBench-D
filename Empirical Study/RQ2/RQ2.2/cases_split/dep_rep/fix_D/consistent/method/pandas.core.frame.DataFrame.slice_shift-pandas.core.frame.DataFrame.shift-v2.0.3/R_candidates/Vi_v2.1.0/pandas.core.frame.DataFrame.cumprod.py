    @doc(make_doc("cumprod", 2))
    def cumprod(self, axis: Axis | None = None, skipna: bool = True, *args, **kwargs):
        return NDFrame.cumprod(self, axis, skipna, *args, **kwargs)
