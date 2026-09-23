class DrawEvent(Event):
    """
    An event triggered by a draw operation on the canvas

    In most backends callbacks subscribed to this callback will be
    fired after the rendering is complete but before the screen is
    updated.  Any extra artists drawn to the canvas's renderer will
    be reflected without an explicit call to ``blit``.

    .. warning::

       Calling ``canvas.draw`` and ``canvas.blit`` in these callbacks may
       not be safe with all backends and may cause infinite recursion.

    In addition to the `Event` attributes, the following event
    attributes are defined:

    Attributes
    ----------
    renderer : `RendererBase`
        The renderer for the draw event.
    """
    def __init__(self, name, canvas, renderer):
        super().__init__(name, canvas)
        self.renderer = renderer
