    @property
    def on_loop_available(self):
        warnings.warn("on_loop_available is deprecated and will be removed",
                      DeprecationWarning, stacklevel=2)
        return self._on_loop_available
