    def pick(self, mouseevent):
        """
        Process a pick event.

        Each child artist will fire a pick event if *mouseevent* is over
        the artist and the artist has picker set.

        See Also
        --------
        set_picker, get_picker, pickable
        """
        # Pick self
        if self.pickable():
            picker = self.get_picker()
            if callable(picker):
                inside, prop = picker(self, mouseevent)
            else:
                inside, prop = self.contains(mouseevent)
            if inside:
                self.figure.canvas.pick_event(mouseevent, self, **prop)

        # Pick children
        for a in self.get_children():
            # make sure the event happened in the same axes
            ax = getattr(a, 'axes', None)
            if (mouseevent.inaxes is None or ax is None
                    or mouseevent.inaxes == ax):
                # we need to check if mouseevent.inaxes is None
                # because some objects associated with an axes (e.g., a
                # tick label) can be outside the bounding box of the
                # axes and inaxes will be None
                # also check that ax is None so that it traverse objects
                # which do no have an axes property but children might
                a.pick(mouseevent)
