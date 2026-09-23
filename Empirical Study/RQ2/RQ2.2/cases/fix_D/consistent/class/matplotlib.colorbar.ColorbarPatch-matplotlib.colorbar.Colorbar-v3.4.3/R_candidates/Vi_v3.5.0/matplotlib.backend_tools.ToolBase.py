class ToolBase:
    """
    Base tool class.

    A base tool, only implements `trigger` method or no method at all.
    The tool is instantiated by `matplotlib.backend_managers.ToolManager`.
    """

    default_keymap = None
    """
    Keymap to associate with this tool.

    ``list[str]``: List of keys that will trigger this tool when a keypress
    event is emitted on ``self.figure.canvas``.
    """

    description = None
    """
    Description of the Tool.

    `str`: Tooltip used if the Tool is included in a Toolbar.
    """

    image = None
    """
    Filename of the image.

    `str`: Filename of the image to use in a Toolbar.  If None, the *name* is
    used as a label in the toolbar button.
    """

    def __init__(self, toolmanager, name):
        self._name = name
        self._toolmanager = toolmanager
        self._figure = None

    name = property(
        lambda self: self._name,
        doc="The tool id (str, must be unique among tools of a tool manager).")
    toolmanager = property(
        lambda self: self._toolmanager,
        doc="The `.ToolManager` that controls this tool.")
    canvas = property(
        lambda self: self._figure.canvas if self._figure is not None else None,
        doc="The canvas of the figure affected by this tool, or None.")

    @property
    def figure(self):
        """The Figure affected by this tool, or None."""
        return self._figure

    @figure.setter
    def figure(self, figure):
        self._figure = figure

    set_figure = figure.fset

    def _make_classic_style_pseudo_toolbar(self):
        """
        Return a placeholder object with a single `canvas` attribute.

        This is useful to reuse the implementations of tools already provided
        by the classic Toolbars.
        """
        return SimpleNamespace(canvas=self.canvas)

    def trigger(self, sender, event, data=None):
        """
        Called when this tool gets used.

        This method is called by `.ToolManager.trigger_tool`.

        Parameters
        ----------
        event : `.Event`
            The canvas event that caused this tool to be called.
        sender : object
            Object that requested the tool to be triggered.
        data : object
            Extra data.
        """
        pass

    def destroy(self):
        """
        Destroy the tool.

        This method is called by `.ToolManager.remove_tool`.
        """
        pass
