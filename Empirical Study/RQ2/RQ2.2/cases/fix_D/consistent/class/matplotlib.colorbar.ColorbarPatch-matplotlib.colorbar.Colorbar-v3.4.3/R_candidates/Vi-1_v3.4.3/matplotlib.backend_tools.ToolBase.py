class ToolBase:
    """
    Base tool class.

    A base tool, only implements `trigger` method or not method at all.
    The tool is instantiated by `matplotlib.backend_managers.ToolManager`.

    Attributes
    ----------
    toolmanager : `matplotlib.backend_managers.ToolManager`
        ToolManager that controls this Tool.
    figure : `FigureCanvas`
        Figure instance that is affected by this Tool.
    name : str
        Used as **Id** of the tool, has to be unique among tools of the same
        ToolManager.
    """

    default_keymap = None
    """
    Keymap to associate with this tool.

    **String**: List of comma separated keys that will be used to call this
    tool when the keypress event of ``self.figure.canvas`` is emitted.
    """

    description = None
    """
    Description of the Tool.

    **String**: If the Tool is included in the Toolbar this text is used
    as a Tooltip.
    """

    image = None
    """
    Filename of the image.

    **String**: Filename of the image to use in the toolbar. If None, the
    *name* is used as a label in the toolbar button.
    """

    def __init__(self, toolmanager, name):
        self._name = name
        self._toolmanager = toolmanager
        self._figure = None

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self.set_figure(figure)

    @property
    def canvas(self):
        if not self._figure:
            return None
        return self._figure.canvas

    @property
    def toolmanager(self):
        return self._toolmanager

    def _make_classic_style_pseudo_toolbar(self):
        """
        Return a placeholder object with a single `canvas` attribute.

        This is useful to reuse the implementations of tools already provided
        by the classic Toolbars.
        """
        return SimpleNamespace(canvas=self.canvas)

    def set_figure(self, figure):
        """
        Assign a figure to the tool.

        Parameters
        ----------
        figure : `.Figure`
        """
        self._figure = figure

    def trigger(self, sender, event, data=None):
        """
        Called when this tool gets used.

        This method is called by
        `matplotlib.backend_managers.ToolManager.trigger_tool`.

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

    @property
    def name(self):
        """Tool Id."""
        return self._name

    def destroy(self):
        """
        Destroy the tool.

        This method is called when the tool is removed by
        `matplotlib.backend_managers.ToolManager.remove_tool`.
        """
        pass
