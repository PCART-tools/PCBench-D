    def trigger(self, sender, event, data=None):
        if event.inaxes is None:
            return

        for a in self.figure.get_axes():
            if (event.x is not None and event.y is not None
                    and a.in_axes(event)):
                a.set_navigate(True)
