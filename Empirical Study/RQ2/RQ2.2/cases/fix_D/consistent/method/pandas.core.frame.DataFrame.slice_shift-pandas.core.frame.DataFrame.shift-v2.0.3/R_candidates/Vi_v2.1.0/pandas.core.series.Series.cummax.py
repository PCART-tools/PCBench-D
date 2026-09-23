    @doc(make_doc("cummax", ndim=1))
    def cummax(self, axis: Axis | None = None, skipna: bool = True, *args, **kwargs):
        return NDFrame.cummax(self, axis, skipna, *args, **kwargs)
