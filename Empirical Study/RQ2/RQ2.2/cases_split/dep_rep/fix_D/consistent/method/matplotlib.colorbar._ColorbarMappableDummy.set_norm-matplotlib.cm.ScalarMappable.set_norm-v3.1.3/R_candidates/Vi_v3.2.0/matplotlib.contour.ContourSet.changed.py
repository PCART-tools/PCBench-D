    def changed(self):
        tcolors = [(tuple(rgba),)
                   for rgba in self.to_rgba(self.cvalues, alpha=self.alpha)]
        self.tcolors = tcolors
        hatches = self.hatches * len(tcolors)
        for color, hatch, collection in zip(tcolors, hatches,
                                            self.collections):
            if self.filled:
                collection.set_facecolor(color)
                # update the collection's hatch (may be None)
                collection.set_hatch(hatch)
            else:
                collection.set_color(color)
        for label, cv in zip(self.labelTexts, self.labelCValues):
            label.set_alpha(self.alpha)
            label.set_color(self.labelMappable.to_rgba(cv))
        # add label colors
        cm.ScalarMappable.changed(self)
