    def _mpl_buttons(self, controller):
        # NOTE: This spews "Broken accounting of active state" warnings on
        # right click on macOS.
        surface = self.get_native().get_surface()
        is_over, x, y, event_state = surface.get_device_position(
            self.get_display().get_default_seat().get_pointer())
        # NOTE: alternatively we could use
        #   event_state = controller.get_current_event_state()
        # but for button_press/button_release this would report the state
        # *prior* to the event rather than after it; the above reports the
        # state *after* it.
        mod_table = [
            (MouseButton.LEFT, Gdk.ModifierType.BUTTON1_MASK),
            (MouseButton.MIDDLE, Gdk.ModifierType.BUTTON2_MASK),
            (MouseButton.RIGHT, Gdk.ModifierType.BUTTON3_MASK),
            (MouseButton.BACK, Gdk.ModifierType.BUTTON4_MASK),
            (MouseButton.FORWARD, Gdk.ModifierType.BUTTON5_MASK),
        ]
        return {name for name, mask in mod_table if event_state & mask}
