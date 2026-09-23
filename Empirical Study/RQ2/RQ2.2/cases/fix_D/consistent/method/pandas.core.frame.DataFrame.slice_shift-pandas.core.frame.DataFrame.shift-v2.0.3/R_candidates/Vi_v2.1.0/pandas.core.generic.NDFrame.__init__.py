    def __init__(self, data: Manager) -> None:
        object.__setattr__(self, "_is_copy", None)
        object.__setattr__(self, "_mgr", data)
        object.__setattr__(self, "_item_cache", {})
        object.__setattr__(self, "_attrs", {})
        object.__setattr__(self, "_flags", Flags(self, allows_duplicate_labels=True))
