    def set_figure(self, figure, update_tools=True):
        """
        Bind the given figure to the tools.

        Parameters
        ----------
        figure : `.Figure`
        update_tools : bool
            Force tools to update figure
        """
        if self._key_press_handler_id:
            self.canvas.mpl_disconnect(self._key_press_handler_id)
        self._figure = figure
        if figure:
            self._key_press_handler_id = self.canvas.mpl_connect(
                'key_press_event', self._key_press)
        if update_tools:
            for tool in self._tools.values():
                tool.figure = figure
