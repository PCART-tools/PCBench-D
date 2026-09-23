    def updateButtonText(self, lst):
        """Update the list of selected axes in the menu button"""
        axis_txt = ''
        for e in lst:
            axis_txt += '%d,' % (e + 1)
        # remove trailing ',' and add to button string
        self.SetLabel("Axes: %s" % axis_txt[:-1])
