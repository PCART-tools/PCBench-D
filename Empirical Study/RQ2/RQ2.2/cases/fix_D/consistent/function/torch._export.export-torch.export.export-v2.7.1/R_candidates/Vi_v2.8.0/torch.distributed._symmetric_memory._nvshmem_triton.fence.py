    @core.extern
    def fence(_builder=None):  # type: ignore[no-untyped-def]
        return core.extern_elementwise(
            "",
            "",
            [],
            {
                (): ("nvshmem_fence", core.dtype("int32")),
            },
            is_pure=False,
            _builder=_builder,
        )
