class _DeprecatedCmapDictWrapper(MutableMapping):
    """Dictionary mapping for deprecated _cmap_d access."""

    def __init__(self, cmap_registry):
        self._cmap_registry = cmap_registry

    def __delitem__(self, key):
        self._warn_deprecated()
        self._cmap_registry.__delitem__(key)

    def __getitem__(self, key):
        self._warn_deprecated()
        return self._cmap_registry.__getitem__(key)

    def __iter__(self):
        self._warn_deprecated()
        return self._cmap_registry.__iter__()

    def __len__(self):
        self._warn_deprecated()
        return self._cmap_registry.__len__()

    def __setitem__(self, key, val):
        self._warn_deprecated()
        self._cmap_registry.__setitem__(key, val)

    def get(self, key, default=None):
        self._warn_deprecated()
        return self._cmap_registry.get(key, default)

    def _warn_deprecated(self):
        _api.warn_deprecated(
            "3.3",
            message="The global colormaps dictionary is no longer "
                    "considered public API.",
            alternative="Please use register_cmap() and get_cmap() to "
                        "access the contents of the dictionary."
        )
