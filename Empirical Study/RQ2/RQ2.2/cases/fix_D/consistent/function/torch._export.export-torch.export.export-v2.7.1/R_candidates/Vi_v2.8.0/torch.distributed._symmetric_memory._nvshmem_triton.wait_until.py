    @core.extern
    def wait_until(ivar, cmp, cmp_val, _builder=None):  # type: ignore[no-untyped-def]
        return core.extern_elementwise(
            "",
            "",
            [ivar, cmp, cmp_val],
            {
                (
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                ): ("nvshmem_longlong_wait_until", core.dtype("int32"))
            },
            is_pure=False,
            _builder=_builder,
        )
