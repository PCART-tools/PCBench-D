    def button_press_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.allocation.height - event.y
        dblclick = (event.type == gdk._2BUTTON_PRESS)
        if not dblclick:
            # GTK is the only backend that generates a DOWN-UP-DOWN-DBLCLICK-UP  event
            # sequence for a double click.  All other backends have a DOWN-UP-DBLCLICK-UP
            # sequence.  In order to provide consistency to matplotlib users, we will
            # eat the extra DOWN event in the case that we detect it is part of a double
            # click.
            # first, get the double click time in milliseconds.
            current_time  = event.get_time()
            last_time     = self.last_downclick.get(event.button,0)
            dblclick_time = gtk.settings_get_for_screen(gdk.screen_get_default()).get_property('gtk-double-click-time')
            delta_time    = current_time-last_time
            if delta_time < dblclick_time:
                del self.last_downclick[event.button] # we do not want to eat more than one event.
                return False                          # eat.
            self.last_downclick[event.button] = current_time
        FigureCanvasBase.button_press_event(self, x, y, event.button, dblclick=dblclick, guiEvent=event)
        return False  # finish event propagation?
