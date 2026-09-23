    def _get_backend_or_none(self):
        """Get the requested backend, if any, without triggering resolution."""
        backend = dict.__getitem__(self, "backend")
        return None if backend is rcsetup._auto_backend_sentinel else backend
