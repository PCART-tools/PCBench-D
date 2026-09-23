    @classmethod
    def _from_mgr(cls, mgr: Manager):
        """
        Fastpath to create a new DataFrame/Series from just a BlockManager/ArrayManager.

        Notes
        -----
        Skips setting `_flags` attribute; caller is responsible for doing so.
        """
        obj = cls.__new__(cls)
        object.__setattr__(obj, "_is_copy", None)
        object.__setattr__(obj, "_mgr", mgr)
        object.__setattr__(obj, "_item_cache", {})
        object.__setattr__(obj, "_attrs", {})
        return obj
