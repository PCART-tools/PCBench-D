    @_api.deprecated(
        "3.9",
        alternative="``matplotlib.backends.backend_registry.list_builtin"
            "(matplotlib.backends.BackendFilter.NON_INTERACTIVE)``")
    @property
    def non_interactive_bk(self):
        return backend_registry.list_builtin(BackendFilter.NON_INTERACTIVE)
