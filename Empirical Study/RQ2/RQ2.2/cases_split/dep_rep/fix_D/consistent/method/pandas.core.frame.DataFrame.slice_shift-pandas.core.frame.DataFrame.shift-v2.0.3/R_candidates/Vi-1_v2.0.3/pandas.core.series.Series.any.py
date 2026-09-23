    @doc(NDFrame.any, **_shared_doc_kwargs)
    def any(  # type: ignore[empty-body]
        self,
        axis: Axis = 0,
        bool_only: bool | None = None,
        skipna: bool = True,
        level: Level | None = None,
        **kwargs,
    ) -> Series | bool:
        ...
