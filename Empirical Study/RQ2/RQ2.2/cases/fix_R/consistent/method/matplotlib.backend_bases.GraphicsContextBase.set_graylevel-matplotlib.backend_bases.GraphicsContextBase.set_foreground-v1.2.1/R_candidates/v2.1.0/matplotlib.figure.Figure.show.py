    def show(self, warn=True):
        """
        If using a GUI backend with pyplot, display the figure window.

        If the figure was not created using
        :func:`~matplotlib.pyplot.figure`, it will lack a
        :class:`~matplotlib.backend_bases.FigureManagerBase`, and
        will raise an AttributeError.

        For non-GUI backends, this does nothing, in which case
        a warning will be issued if *warn* is True (default).
        """
        try:
            manager = getattr(self.canvas, 'manager')
        except AttributeError as err:
            raise AttributeError("%s\n"
                                 "Figure.show works only "
                                 "for figures managed by pyplot, normally "
                                 "created by pyplot.figure()." % err)

        if manager is not None:
            try:
                manager.show()
                return
            except NonGuiException:
                pass
        if warn:
            import warnings
            warnings.warn(
                "matplotlib is currently using a non-GUI backend, "
                "so cannot show the figure")
