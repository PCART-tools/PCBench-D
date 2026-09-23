    def _backend_module_name(self, backend):
        # Return name of module containing the specified backend.
        # Does not check if the backend is valid, use is_valid_backend for that.
        backend = backend.lower()

        # Check if have specific name to module mapping.
        backend = self._name_to_module.get(backend, backend)

        return (backend[9:] if backend.startswith("module://")
                else f"matplotlib.backends.backend_{backend}")
