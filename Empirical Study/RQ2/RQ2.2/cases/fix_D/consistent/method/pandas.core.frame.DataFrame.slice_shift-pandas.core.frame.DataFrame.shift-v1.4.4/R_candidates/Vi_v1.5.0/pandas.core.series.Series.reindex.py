    @doc(
        NDFrame.reindex,  # type: ignore[has-type]
        klass=_shared_doc_kwargs["klass"],
        axes=_shared_doc_kwargs["axes"],
        optional_labels=_shared_doc_kwargs["optional_labels"],
        optional_axis=_shared_doc_kwargs["optional_axis"],
    )
    def reindex(self, *args, **kwargs) -> Series:
        if len(args) > 1:
            raise TypeError("Only one positional argument ('index') is allowed")
        if args:
            (index,) = args
            if "index" in kwargs:
                raise TypeError(
                    "'index' passed as both positional and keyword argument"
                )
            kwargs.update({"index": index})
        return super().reindex(**kwargs)
