    @_api.rename_parameter("3.8", "trans", "t")
    def set_transform(self, t):
        super().set_transform(t)
        # the text does not get the transform!
        self.stale = True
