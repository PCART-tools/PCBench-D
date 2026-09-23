    def __init__(
        self,
        data: Manager,
        copy: bool_t = False,
        attrs: Mapping[Hashable, Any] | None = None,
    ):
        # copy kwarg is retained for mypy compat, is not used

        object.__setattr__(self, "_is_copy", None)
        object.__setattr__(self, "_mgr", data)
        object.__setattr__(self, "_item_cache", {})
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)
        object.__setattr__(self, "_attrs", attrs)
        object.__setattr__(self, "_flags", Flags(self, allows_duplicate_labels=True))
