    @property
    def visible(self):
        _api.warn_deprecated("3.8", alternative="get_visible")
        return self.get_visible()
