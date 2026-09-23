    def trigger(self, sender, event, data=None):
        if event.inaxes is None:
            return
        ToolToggleBase.trigger(self, sender, event, data)
