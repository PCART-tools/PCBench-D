    def button_press(self, event):
        """The default Matplotlib button actions for extra mouse buttons."""
        if rcParams['toolbar'] != 'toolmanager':
            button_press_handler(event)
