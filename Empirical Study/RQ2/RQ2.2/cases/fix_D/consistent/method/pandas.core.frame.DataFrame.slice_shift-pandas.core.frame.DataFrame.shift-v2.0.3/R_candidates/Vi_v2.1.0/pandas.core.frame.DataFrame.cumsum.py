    @doc(make_doc("cumsum", ndim=2))
    def cumsum(self, axis: Axis | None = None, skipna: bool = True, *args, **kwargs):
        return NDFrame.cumsum(self, axis, skipna, *args, **kwargs)
