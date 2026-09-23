    def pick(self, mouseevent):
        """
        Process a pick event.

        Each child artist will fire a pick event if *mouseevent* is over
        the artist and the artist has picker set.

        See Also
        --------
        set_picker, get_picker, pickable
        """
        from .backend_bases import PickEvent  # Circular import.
        # Pick self
        if self.pickable():
            picker = self.get_picker()
            if callable(picker):
                inside, prop = picker(self, mouseevent)
            else:
                inside, prop = self.contains(mouseevent)
            if inside:
                PickEvent("pick_event", self.figure.canvas,
                          mouseevent, self, **prop)._process()

        # Pick children
        for a in self.get_children():
            # make sure the event happened in the same Axes
            ax = getattr(a, 'axes', None)
            if (mouseevent.inaxes is None or ax is None
                    or mouseevent.inaxes == ax):
                # we need to check if mouseevent.inaxes is None
                # because some objects associated with an Axes (e.g., a
                # tick label) can be outside the bounding box of the
                # Axes and inaxes will be None
                # also check that ax is None so that it traverse objects
                # which do no have an axes property but children might
                a.pick(mouseevent)
