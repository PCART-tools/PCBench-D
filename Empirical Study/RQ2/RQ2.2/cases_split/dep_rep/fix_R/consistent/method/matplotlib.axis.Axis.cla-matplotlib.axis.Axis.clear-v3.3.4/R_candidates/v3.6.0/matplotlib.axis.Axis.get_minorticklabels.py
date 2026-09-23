    def get_minorticklabels(self):
        """Return this Axis' minor tick labels, as a list of `~.text.Text`."""
        self._update_ticks()
        ticks = self.get_minor_ticks()
        labels1 = [tick.label1 for tick in ticks if tick.label1.get_visible()]
        labels2 = [tick.label2 for tick in ticks if tick.label2.get_visible()]
        return labels1 + labels2
