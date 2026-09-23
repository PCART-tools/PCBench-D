    def key_press(self, event):
        """
        Implement the default Matplotlib key bindings defined at
        :ref:`key-event-handling`.
        """
        if rcParams['toolbar'] != 'toolmanager':
            key_press_handler(event, self.canvas, self.canvas.toolbar)
