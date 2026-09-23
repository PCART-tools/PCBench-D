    @_api.deprecated(
        "3.9",
        alternative="``matplotlib.backends.backend_registry.list_builtin()``")
    @property
    def all_backends(self):
        return backend_registry.list_builtin()
