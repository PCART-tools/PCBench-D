    def _add_box(self):
        self._box = RectangleSelector(self.ax,
                                      useblit=self.useblit,
                                      grab_range=self.grab_range,
                                      handle_props=self._box_handle_props,
                                      props=self._box_props,
                                      interactive=True)
        self._box._state_modifier_keys.pop('rotate')
        self._box.connect_event('motion_notify_event', self._scale_polygon)
        self._update_box()
        # Set state that prevents the RectangleSelector from being created
        # by the user
        self._box._allow_creation = False
        self._box._selection_completed = True
        self._draw_polygon()
