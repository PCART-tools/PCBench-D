    @visible.setter
    def visible(self, visible):
        _api.warn_deprecated("3.6", alternative="set_visible")
        self.set_visible(visible)
