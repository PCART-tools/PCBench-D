    class Toolbar(NavigationToolbar2Tk):
        # Only display the buttons we need.
        toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                     t[0] in ('Home', 'Pan', 'Zoom')]
