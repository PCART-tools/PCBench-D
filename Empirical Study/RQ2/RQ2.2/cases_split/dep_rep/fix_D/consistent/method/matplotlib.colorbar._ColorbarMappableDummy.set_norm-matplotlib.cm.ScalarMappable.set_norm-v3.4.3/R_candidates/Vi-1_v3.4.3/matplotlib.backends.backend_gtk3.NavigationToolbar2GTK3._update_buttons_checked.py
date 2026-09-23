    def _update_buttons_checked(self):
        for name, active in [("Pan", "PAN"), ("Zoom", "ZOOM")]:
            button = self._gtk_ids.get(name)
            if button:
                with button.handler_block(button._signal_handler):
                    button.set_active(self.mode.name == active)
