    @_api.rename_parameter("3.8", "event", "mouseevent")
    def contains(self, mouseevent):
        return self.legendPatch.contains(mouseevent)
