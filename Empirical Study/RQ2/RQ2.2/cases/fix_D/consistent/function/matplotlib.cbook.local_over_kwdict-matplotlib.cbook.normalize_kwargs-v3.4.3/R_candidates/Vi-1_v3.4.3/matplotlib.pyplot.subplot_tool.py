def subplot_tool(targetfig=None):
    """
    Launch a subplot tool window for a figure.

    A `matplotlib.widgets.SubplotTool` instance is returned. You must maintain
    a reference to the instance to keep the associated callbacks alive.
    """
    if targetfig is None:
        targetfig = gcf()
    with rc_context({"toolbar": "none"}):  # No navbar for the toolfig.
        # Use new_figure_manager() instead of figure() so that the figure
        # doesn't get registered with pyplot.
        manager = new_figure_manager(-1, (6, 3))
    manager.set_window_title("Subplot configuration tool")
    tool_fig = manager.canvas.figure
    tool_fig.subplots_adjust(top=0.9)
    manager.show()
    return SubplotTool(targetfig, tool_fig)
