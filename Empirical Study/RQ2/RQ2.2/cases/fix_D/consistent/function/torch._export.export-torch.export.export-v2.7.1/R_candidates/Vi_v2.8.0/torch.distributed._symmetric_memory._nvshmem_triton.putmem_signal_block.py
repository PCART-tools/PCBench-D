    @core.extern
    def putmem_signal_block(  # type: ignore[no-untyped-def]
        dst,
        src,
        nelems,
        sig_addr,
        signal,
        sig_op,
        pe,
        _builder=None,
    ):  # type: ignore[no-untyped-def]
        return core.extern_elementwise(
            "",
            "",
            [dst, src, nelems, sig_addr, signal, sig_op, pe],
            {
                (
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                ): ("nvshmemx_putmem_signal_block", core.dtype("int32"))
            },
            is_pure=False,
            _builder=_builder,
        )
