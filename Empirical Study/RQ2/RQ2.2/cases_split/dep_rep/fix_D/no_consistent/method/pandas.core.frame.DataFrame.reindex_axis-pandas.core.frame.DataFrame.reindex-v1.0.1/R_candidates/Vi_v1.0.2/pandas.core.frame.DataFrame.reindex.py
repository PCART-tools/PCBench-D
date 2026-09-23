    @Substitution(**_shared_doc_kwargs)
    @Appender(NDFrame.reindex.__doc__)
    @rewrite_axis_style_signature(
        "labels",
        [
            ("method", None),
            ("copy", True),
            ("level", None),
            ("fill_value", np.nan),
            ("limit", None),
            ("tolerance", None),
        ],
    )
    def reindex(self, *args, **kwargs) -> "DataFrame":
        axes = validate_axis_style_args(self, args, kwargs, "labels", "reindex")
        kwargs.update(axes)
        # Pop these, since the values are in `kwargs` under different names
        kwargs.pop("axis", None)
        kwargs.pop("labels", None)
        return super().reindex(**kwargs)
