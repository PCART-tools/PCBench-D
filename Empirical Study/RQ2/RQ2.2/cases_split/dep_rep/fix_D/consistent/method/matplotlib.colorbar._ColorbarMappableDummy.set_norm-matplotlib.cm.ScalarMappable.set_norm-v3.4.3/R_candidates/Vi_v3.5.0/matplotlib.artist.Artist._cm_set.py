    @contextlib.contextmanager
    def _cm_set(self, **kwargs):
        """
        `.Artist.set` context-manager that restores original values at exit.
        """
        orig_vals = {k: getattr(self, f"get_{k}")() for k in kwargs}
        try:
            self.set(**kwargs)
            yield
        finally:
            self.set(**orig_vals)
