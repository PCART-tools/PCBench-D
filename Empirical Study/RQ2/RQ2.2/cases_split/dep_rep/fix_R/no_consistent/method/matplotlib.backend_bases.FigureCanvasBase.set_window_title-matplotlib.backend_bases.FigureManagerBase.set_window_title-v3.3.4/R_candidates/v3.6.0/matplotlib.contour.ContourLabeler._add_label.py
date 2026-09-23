    def _add_label(self, t, x, y, lev, cvalue):
        color = self.labelMappable.to_rgba(cvalue, alpha=self.alpha)

        _text = self.get_text(lev, self.labelFmt)
        self.set_label_props(t, _text, color)
        self.labelTexts.append(t)
        self.labelCValues.append(cvalue)
        self.labelXYs.append((x, y))

        # Add label to plot here - useful for manual mode label selection
        self.axes.add_artist(t)
