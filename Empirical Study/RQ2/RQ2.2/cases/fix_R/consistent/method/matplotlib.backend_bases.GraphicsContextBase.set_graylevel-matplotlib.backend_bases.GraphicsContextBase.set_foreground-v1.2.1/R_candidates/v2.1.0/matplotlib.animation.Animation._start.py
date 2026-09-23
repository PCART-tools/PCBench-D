    def _start(self, *args):
        '''
        Starts interactive animation. Adds the draw frame command to the GUI
        handler, calls show to start the event loop.
        '''
        # First disconnect our draw event handler
        self._fig.canvas.mpl_disconnect(self._first_draw_id)
        self._first_draw_id = None  # So we can check on save

        # Now do any initial draw
        self._init_draw()

        # Add our callback for stepping the animation and
        # actually start the event_source.
        self.event_source.add_callback(self._step)
        self.event_source.start()
