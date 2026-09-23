    @doc(NDFrame.any, **_shared_doc_kwargs)
    def any(
        self,
        axis: Axis = 0,
        bool_only: bool | None = None,
        skipna: bool = True,
        level: Level = None,
        **kwargs,
    ) -> DataFrame | Series:
        ...
