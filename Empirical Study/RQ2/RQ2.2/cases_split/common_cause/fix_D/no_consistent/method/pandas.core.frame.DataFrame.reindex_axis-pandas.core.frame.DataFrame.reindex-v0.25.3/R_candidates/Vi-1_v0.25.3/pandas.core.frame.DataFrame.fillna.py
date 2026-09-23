    @Substitution(**_shared_doc_kwargs)
    @Appender(NDFrame.fillna.__doc__)
    def fillna(
        self,
        value=None,
        method=None,
        axis=None,
        inplace=False,
        limit=None,
        downcast=None,
        **kwargs
    ):
        return super().fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
            **kwargs
        )
