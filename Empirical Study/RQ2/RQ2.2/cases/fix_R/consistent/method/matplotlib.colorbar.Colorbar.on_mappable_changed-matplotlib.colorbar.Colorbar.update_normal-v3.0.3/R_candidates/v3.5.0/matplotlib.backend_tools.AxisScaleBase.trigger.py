    def trigger(self, sender, event, data=None):
        if event.inaxes is None:
            return
        super().trigger(sender, event, data)
