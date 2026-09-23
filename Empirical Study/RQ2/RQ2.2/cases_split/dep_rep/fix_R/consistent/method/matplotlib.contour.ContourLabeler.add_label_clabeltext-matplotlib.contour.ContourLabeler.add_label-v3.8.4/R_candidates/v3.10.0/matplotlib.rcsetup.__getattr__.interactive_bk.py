    @_api.deprecated(
        "3.9",
        alternative="``matplotlib.backends.backend_registry.list_builtin"
            "(matplotlib.backends.BackendFilter.INTERACTIVE)``")
    @property
    def interactive_bk(self):
        return backend_registry.list_builtin(BackendFilter.INTERACTIVE)
