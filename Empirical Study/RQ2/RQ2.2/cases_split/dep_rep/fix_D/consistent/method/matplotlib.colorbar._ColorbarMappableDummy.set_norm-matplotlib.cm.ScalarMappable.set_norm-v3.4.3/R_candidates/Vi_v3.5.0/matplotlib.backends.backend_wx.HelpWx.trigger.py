    def trigger(self, *args):
        _HelpDialog.show(self.figure.canvas.GetTopLevelParent(),
                         self._get_help_entries())
