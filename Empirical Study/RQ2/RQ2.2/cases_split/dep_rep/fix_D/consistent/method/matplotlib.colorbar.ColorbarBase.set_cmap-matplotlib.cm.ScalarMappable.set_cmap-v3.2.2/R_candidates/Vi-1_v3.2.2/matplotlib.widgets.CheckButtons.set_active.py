    def set_active(self, index):
        """
        Directly (de)activate a check button by index.

        *index* is an index into the original label list
            that this object was constructed with.
            Raises ValueError if *index* is invalid.

        Callbacks will be triggered if :attr:`eventson` is True.
        """
        if not 0 <= index < len(self.labels):
            raise ValueError("Invalid CheckButton index: %d" % index)

        l1, l2 = self.lines[index]
        l1.set_visible(not l1.get_visible())
        l2.set_visible(not l2.get_visible())

        if self.drawon:
            self.ax.figure.canvas.draw()

        if not self.eventson:
            return
        for cid, func in self.observers.items():
            func(self.labels[index].get_text())
