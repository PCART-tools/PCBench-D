    def __init__(self, ax, onselect, useblit=False,
                 lineprops=None, markerprops=None, vertex_select_radius=15):
        # The state modifiers 'move', 'square', and 'center' are expected by
        # _SelectorWidget but are not supported by PolygonSelector
        # Note: could not use the existing 'move' state modifier in-place of
        # 'move_all' because _SelectorWidget automatically discards 'move'
        # from the state on button release.
        state_modifier_keys = dict(clear='escape', move_vertex='control',
                                   move_all='shift', move='not-applicable',
                                   square='not-applicable',
                                   center='not-applicable')
        _SelectorWidget.__init__(self, ax, onselect, useblit=useblit,
                                 state_modifier_keys=state_modifier_keys)

        self._xs, self._ys = [0], [0]
        self._polygon_completed = False

        if lineprops is None:
            lineprops = dict(color='k', linestyle='-', linewidth=2, alpha=0.5)
        lineprops['animated'] = self.useblit
        self.line = Line2D(self._xs, self._ys, **lineprops)
        self.ax.add_line(self.line)

        if markerprops is None:
            markerprops = dict(mec='k', mfc=lineprops.get('color', 'k'))
        self._polygon_handles = ToolHandles(self.ax, self._xs, self._ys,
                                            useblit=self.useblit,
                                            marker_props=markerprops)

        self._active_handle_idx = -1
        self.vertex_select_radius = vertex_select_radius

        self.artists = [self.line, self._polygon_handles.artist]
        self.set_visible(True)
