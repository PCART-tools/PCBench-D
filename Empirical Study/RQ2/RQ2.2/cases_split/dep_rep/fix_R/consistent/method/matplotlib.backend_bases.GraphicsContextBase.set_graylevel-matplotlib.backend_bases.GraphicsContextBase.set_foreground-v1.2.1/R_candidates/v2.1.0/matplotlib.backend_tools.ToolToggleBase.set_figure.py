    def set_figure(self, figure):
        toggled = self.toggled
        if toggled:
            if self.figure:
                self.trigger(self, None)
            else:
                # if no figure the internal state is not changed
                # we change it here so next call to trigger will change it back
                self._toggled = False
        ToolBase.set_figure(self, figure)
        if toggled:
            if figure:
                self.trigger(self, None)
            else:
                # if there is no figure, triggen wont change the internal state
                # we change it back
                self._toggled = True
