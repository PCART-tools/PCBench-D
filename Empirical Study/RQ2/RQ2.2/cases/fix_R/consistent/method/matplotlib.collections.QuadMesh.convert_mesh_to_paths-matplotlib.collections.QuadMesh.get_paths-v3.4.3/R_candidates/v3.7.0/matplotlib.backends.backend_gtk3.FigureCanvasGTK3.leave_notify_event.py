    def leave_notify_event(self, widget, event):
        gtk_mods = Gdk.Keymap.get_for_display(
            self.get_display()).get_modifier_state()
        LocationEvent("figure_leave_event", self, *self._mpl_coords(event),
                      modifiers=self._mpl_modifiers(gtk_mods),
                      guiEvent=event)._process()
