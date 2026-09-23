    def _update_enter_leave(self):
        'process the figure/axes enter leave events'
        if LocationEvent.lastevent is not None:
            last = LocationEvent.lastevent
            if last.inaxes != self.inaxes:
                # process axes enter/leave events
                try:
                    if last.inaxes is not None:
                        last.canvas.callbacks.process('axes_leave_event', last)
                except:
                    pass
                    # See ticket 2901582.
                    # I think this is a valid exception to the rule
                    # against catching all exceptions; if anything goes
                    # wrong, we simply want to move on and process the
                    # current event.
                if self.inaxes is not None:
                    self.canvas.callbacks.process('axes_enter_event', self)

        else:
            # process a figure enter event
            if self.inaxes is not None:
                self.canvas.callbacks.process('axes_enter_event', self)

        LocationEvent.lastevent = self
