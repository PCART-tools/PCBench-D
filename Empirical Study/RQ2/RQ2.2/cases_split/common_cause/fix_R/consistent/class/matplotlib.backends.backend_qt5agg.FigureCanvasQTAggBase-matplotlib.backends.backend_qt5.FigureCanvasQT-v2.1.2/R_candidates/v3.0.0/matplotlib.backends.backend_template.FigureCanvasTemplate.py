class FigureCanvasTemplate(FigureCanvasBase):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc.

    Note: GUI templates will want to connect events for button presses,
    mouse movements and key presses to functions that call the base
    class methods button_press_event, button_release_event,
    motion_notify_event, key_press_event, and key_release_event.  See the
    implementations of the interactive backends for examples.

    Attributes
    ----------
    figure : `matplotlib.figure.Figure`
        A high-level Figure instance
    """

    def draw(self):
        """
        Draw the figure using the renderer
        """
        renderer = RendererTemplate(self.figure.dpi)
        self.figure.draw(renderer)

    # You should provide a print_xxx function for every file format
    # you can write.

    # If the file type is not in the base set of filetypes,
    # you should add it to the class-scope filetypes dictionary as follows:
    filetypes = FigureCanvasBase.filetypes.copy()
    filetypes['foo'] = 'My magic Foo format'

    def print_foo(self, filename, *args, **kwargs):
        """
        Write out format foo.  The dpi, facecolor and edgecolor are restored
        to their original values after this call, so you don't need to
        save and restore them.
        """
        pass

    def get_default_filetype(self):
        return 'foo'
