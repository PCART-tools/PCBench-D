    @_api.deprecated(
        "3.4", alternative="get_position()")
    @property
    def figbox(self):
        return self.get_position()
