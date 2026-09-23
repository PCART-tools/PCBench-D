    def toggle_label(self, b):
        axis = self.axis[self.orientation]
        axis.toggle(ticklabels=b, label=b)
