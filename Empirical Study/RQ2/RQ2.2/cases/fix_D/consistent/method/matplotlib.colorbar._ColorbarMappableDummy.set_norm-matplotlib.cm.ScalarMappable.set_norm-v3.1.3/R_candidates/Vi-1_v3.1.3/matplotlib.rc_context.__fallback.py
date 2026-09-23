    def __fallback(self):
        # If anything goes wrong, revert to the original rcs.
        updated_backend = self._orig['backend']
        dict.update(rcParams, self._orig)
        # except for the backend.  If the context block triggered resolving
        # the auto backend resolution keep that value around
        if self._orig['backend'] is rcsetup._auto_backend_sentinel:
            rcParams['backend'] = updated_backend
