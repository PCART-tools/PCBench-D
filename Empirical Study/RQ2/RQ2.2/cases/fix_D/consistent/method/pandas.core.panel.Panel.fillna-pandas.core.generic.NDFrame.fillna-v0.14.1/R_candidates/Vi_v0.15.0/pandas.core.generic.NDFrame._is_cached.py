    @property
    def _is_cached(self):
        """ boolean : return if I am cached """
        return getattr(self, '_cacher', None) is not None
