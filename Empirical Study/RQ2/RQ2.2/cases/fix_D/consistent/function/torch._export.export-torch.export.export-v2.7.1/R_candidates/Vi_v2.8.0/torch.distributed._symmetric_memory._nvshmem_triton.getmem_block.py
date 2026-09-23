    @core.extern
    def getmem_block(dst, src, nelems, pe, _builder=None):  # type: ignore[no-untyped-def]
        return core.extern_elementwise(
            "",
            "",
            [dst, src, nelems, pe],
            {
                (
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                ): ("nvshmemx_getmem_block", core.dtype("int32"))
            },
            is_pure=False,
            _builder=_builder,
        )
