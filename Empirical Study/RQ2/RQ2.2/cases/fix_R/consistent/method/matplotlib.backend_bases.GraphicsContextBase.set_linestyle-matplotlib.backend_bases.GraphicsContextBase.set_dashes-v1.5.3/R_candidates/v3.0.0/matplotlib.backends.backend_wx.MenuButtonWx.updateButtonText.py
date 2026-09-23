    def updateButtonText(self, lst):
        """Update the list of selected axes in the menu button."""
        self.SetLabel(
            'Axes: ' + ','.join('%d' % (e + 1) for e in lst))
