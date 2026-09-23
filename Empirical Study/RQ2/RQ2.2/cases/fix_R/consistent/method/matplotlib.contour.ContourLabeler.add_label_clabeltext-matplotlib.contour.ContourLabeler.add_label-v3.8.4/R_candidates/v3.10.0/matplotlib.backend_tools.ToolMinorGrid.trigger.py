    def trigger(self, sender, event, data=None):
        sentinel = str(uuid.uuid4())
        # Trigger grid switching by temporarily setting :rc:`keymap.grid_minor`
        # to a unique key and sending an appropriate event.
        with (cbook._setattr_cm(event, key=sentinel),
              mpl.rc_context({'keymap.grid_minor': sentinel})):
            mpl.backend_bases.key_press_handler(event, self.figure.canvas)
