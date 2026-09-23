    @property
    def _is_cached(self):
        """ boolean : return if I am cached """
        cacher = getattr(self, '_cacher', None)
        return cacher is not None
