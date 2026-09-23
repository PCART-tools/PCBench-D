    def finish(self):
        """Finish any processing for writing the movie."""
        overridden_cleanup = _api.deprecate_method_override(
            __class__.cleanup, self, since="3.4", alternative="finish()")
        if overridden_cleanup is not None:
            overridden_cleanup()
        else:
            self._cleanup()  # Inline _cleanup() once cleanup() is removed.
