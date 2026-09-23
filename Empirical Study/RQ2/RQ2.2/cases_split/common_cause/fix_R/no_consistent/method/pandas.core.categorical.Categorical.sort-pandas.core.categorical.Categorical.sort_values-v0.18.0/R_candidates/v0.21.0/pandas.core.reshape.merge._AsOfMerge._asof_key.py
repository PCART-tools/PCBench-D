    @property
    def _asof_key(self):
        """ This is our asof key, the 'on' """
        return self.left_on[-1]
