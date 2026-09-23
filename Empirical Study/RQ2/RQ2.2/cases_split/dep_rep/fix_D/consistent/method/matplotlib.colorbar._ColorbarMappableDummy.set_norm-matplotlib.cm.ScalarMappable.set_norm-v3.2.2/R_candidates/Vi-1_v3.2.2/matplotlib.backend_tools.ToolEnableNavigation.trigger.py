    def trigger(self, sender, event, data=None):
        if event.inaxes is None:
            return

        n = int(event.key) - 1
        if n < len(self.figure.get_axes()):
            for i, a in enumerate(self.figure.get_axes()):
                if (event.x is not None and event.y is not None
                        and a.in_axes(event)):
                    a.set_navigate(i == n)
