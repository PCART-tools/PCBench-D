    def show(self):
        'populate the combo box'
        self._updateson = False
        # flush the old
        cbox = self.cbox_lineprops
        for i in range(self._lastcnt-1,-1,-1):
            cbox.remove_text(i)

        # add the new
        for line in self.lines:
            cbox.append_text(line.get_label())
        cbox.set_active(0)

        self._updateson = True
        self._lastcnt = len(self.lines)
        self.dlg.show()
