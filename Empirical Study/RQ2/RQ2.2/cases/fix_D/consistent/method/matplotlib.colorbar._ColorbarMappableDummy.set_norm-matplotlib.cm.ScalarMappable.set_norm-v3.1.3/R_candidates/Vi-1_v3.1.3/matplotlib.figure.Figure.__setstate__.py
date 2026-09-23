    def __setstate__(self, state):
        version = state.pop('__mpl_version__')
        restore_to_pylab = state.pop('_restore_to_pylab', False)

        if version != _mpl_version:
            cbook._warn_external(
                f"This figure was saved with matplotlib version {version} and "
                f"is unlikely to function correctly.")

        self.__dict__ = state

        # re-initialise some of the unstored state information
        self._axobservers = []
        self.canvas = None
        self._layoutbox = None

        if restore_to_pylab:
            # lazy import to avoid circularity
            import matplotlib.pyplot as plt
            import matplotlib._pylab_helpers as pylab_helpers
            allnums = plt.get_fignums()
            num = max(allnums) + 1 if allnums else 1
            mgr = plt._backend_mod.new_figure_manager_given_figure(num, self)

            # XXX The following is a copy and paste from pyplot. Consider
            # factoring to pylab_helpers

            if self.get_label():
                mgr.set_window_title(self.get_label())

            # make this figure current on button press event
            def make_active(event):
                pylab_helpers.Gcf.set_active(mgr)

            mgr._cidgcf = mgr.canvas.mpl_connect('button_press_event',
                                                 make_active)

            pylab_helpers.Gcf.set_active(mgr)
            self.number = num

            plt.draw_if_interactive()
        self.stale = True
