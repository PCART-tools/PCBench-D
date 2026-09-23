    def __len__(self):
        self._warn_deprecated()
        return self._cmap_registry.__len__()
