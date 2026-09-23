    @core.extern
    def signal_wait_until(sig_addr, cmp, cmp_val, _builder=None):  # type: ignore[no-untyped-def]
        return core.extern_elementwise(
            "",
            "",
            [sig_addr, cmp, cmp_val],
            {
                (
                    core.dtype("int64"),
                    core.dtype("int64"),
                    core.dtype("int64"),
                ): ("nvshmem_signal_wait_until", core.dtype("int32"))
            },
            is_pure=False,
            _builder=_builder,
        )
