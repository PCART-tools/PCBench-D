    def get_active_line(self):
        'get the active line'
        ind = self.cbox_lineprops.get_active()
        line = self.lines[ind]
        return line
