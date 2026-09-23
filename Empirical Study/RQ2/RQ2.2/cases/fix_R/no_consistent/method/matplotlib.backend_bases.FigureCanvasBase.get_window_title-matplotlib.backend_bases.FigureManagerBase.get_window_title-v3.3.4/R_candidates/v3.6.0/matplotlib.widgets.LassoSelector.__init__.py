    @_api.rename_parameter("3.5", "lineprops", "props")
    def __init__(self, ax, onselect=None, useblit=True, props=None,
                 button=None):
        super().__init__(ax, onselect, useblit=useblit, button=button)
        self.verts = None
        if props is None:
            props = dict()
        # self.useblit may be != useblit, if the canvas doesn't support blit.
        props.update(animated=self.useblit, visible=False)
        line = Line2D([], [], **props)
        self.ax.add_line(line)
        self._selection_artist = line
