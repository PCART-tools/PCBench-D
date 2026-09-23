class KeyEvent(LocationEvent):
    """
    A key event (key press, key release).

    Attach additional attributes as defined in
    :meth:`FigureCanvasBase.mpl_connect`.

    In addition to the `Event` and `LocationEvent`
    attributes, the following attributes are defined:

    Attributes
    ----------
    key : None or str
        the key(s) pressed. Could be **None**, a single case sensitive ascii
        character ("g", "G", "#", etc.), a special key
        ("control", "shift", "f1", "up", etc.) or a
        combination of the above (e.g., "ctrl+alt+g", "ctrl+alt+G").

    Notes
    -----
    Modifier keys will be prefixed to the pressed key and will be in the order
    "ctrl", "alt", "super". The exception to this rule is when the pressed key
    is itself a modifier key, therefore "ctrl+alt" and "alt+control" can both
    be valid key values.

    Examples
    --------
    ::

        def on_key(event):
            print('you pressed', event.key, event.xdata, event.ydata)

        cid = fig.canvas.mpl_connect('key_press_event', on_key)
    """
    def __init__(self, name, canvas, key, x=0, y=0, guiEvent=None):
        self.key = key
        # super-init deferred to the end: callback errors if called before
        super().__init__(name, canvas, x, y, guiEvent=guiEvent)
