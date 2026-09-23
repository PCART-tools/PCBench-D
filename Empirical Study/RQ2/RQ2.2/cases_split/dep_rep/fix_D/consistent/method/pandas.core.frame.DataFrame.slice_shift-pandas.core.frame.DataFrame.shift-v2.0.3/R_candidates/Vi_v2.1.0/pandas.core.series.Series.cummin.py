    @doc(make_doc("cummin", ndim=1))
    def cummin(self, axis: Axis | None = None, skipna: bool = True, *args, **kwargs):
        return NDFrame.cummin(self, axis, skipna, *args, **kwargs)
