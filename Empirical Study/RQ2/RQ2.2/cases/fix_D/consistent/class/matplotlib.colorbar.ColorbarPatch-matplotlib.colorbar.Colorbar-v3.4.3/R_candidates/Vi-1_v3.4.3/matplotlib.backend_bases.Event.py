class Event:
    """
    A Matplotlib event.  Attach additional attributes as defined in
    :meth:`FigureCanvasBase.mpl_connect`.  The following attributes
    are defined and shown with their default values

    Attributes
    ----------
    name : str
        The event name.
    canvas : `FigureCanvasBase`
        The backend-specific canvas instance generating the event.
    guiEvent
        The GUI event that triggered the Matplotlib event.
    """
    def __init__(self, name, canvas, guiEvent=None):
        self.name = name
        self.canvas = canvas
        self.guiEvent = guiEvent
