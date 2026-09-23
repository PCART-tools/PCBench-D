    def _ensure_has_backend(self):
        """
        Ensure that a "backend" entry exists.

        Normally, the default matplotlibrc file contains *no* entry for "backend" (the
        corresponding line starts with ##, not #; we fill in _auto_backend_sentinel
        in that case.  However, packagers can set a different default backend
        (resulting in a normal `#backend: foo` line) in which case we should *not*
        fill in _auto_backend_sentinel.
        """
        dict.setdefault(self, "backend", rcsetup._auto_backend_sentinel)
