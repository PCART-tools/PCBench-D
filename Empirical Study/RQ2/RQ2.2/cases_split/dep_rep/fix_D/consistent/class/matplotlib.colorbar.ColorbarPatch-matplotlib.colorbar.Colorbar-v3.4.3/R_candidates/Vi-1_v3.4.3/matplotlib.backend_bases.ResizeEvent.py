class ResizeEvent(Event):
    """
    An event triggered by a canvas resize

    In addition to the `Event` attributes, the following event
    attributes are defined:

    Attributes
    ----------
    width : int
        Width of the canvas in pixels.
    height : int
        Height of the canvas in pixels.
    """
    def __init__(self, name, canvas):
        super().__init__(name, canvas)
        self.width, self.height = canvas.get_width_height()
