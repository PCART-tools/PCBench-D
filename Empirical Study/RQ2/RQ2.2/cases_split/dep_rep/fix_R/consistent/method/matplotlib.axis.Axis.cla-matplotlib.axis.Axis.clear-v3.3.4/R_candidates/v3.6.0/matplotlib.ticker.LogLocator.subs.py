    @_api.deprecated("3.6", alternative='set_params(subs=...)')
    def subs(self, subs):
        """
        Set the minor ticks for the log scaling every ``base**i*subs[j]``.
        """
        self._set_subs(subs)
