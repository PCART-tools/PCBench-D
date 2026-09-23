    @doc(NDFrame.rename_axis)
    def rename_axis(  # type: ignore[override]
        self: Series,
        mapper: IndexLabel | lib.NoDefault = lib.no_default,
        *,
        index=lib.no_default,
        axis: Axis = 0,
        copy: bool = True,
        inplace: bool = False,
    ) -> Series | None:
        return super().rename_axis(
            mapper=mapper,
            index=index,
            axis=axis,
            copy=copy,
            inplace=inplace,
        )
