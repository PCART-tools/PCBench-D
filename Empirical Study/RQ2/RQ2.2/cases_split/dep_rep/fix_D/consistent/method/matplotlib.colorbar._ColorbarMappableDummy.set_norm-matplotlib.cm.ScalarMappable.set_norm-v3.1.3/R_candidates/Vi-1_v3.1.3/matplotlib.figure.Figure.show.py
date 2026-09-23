    def show(self, warn=True):
        """
        If using a GUI backend with pyplot, display the figure window.

        If the figure was not created using
        :func:`~matplotlib.pyplot.figure`, it will lack a
        :class:`~matplotlib.backend_bases.FigureManagerBase`, and
        will raise an AttributeError.

        .. warning::
            This does not manage an GUI event loop. Consequently, the figure
            may only be shown briefly or not shown at all if you or your
            environment are not managing an event loop.

            Proper use cases for `.Figure.show` include running this from a
            GUI application or an IPython shell.

            If you're running a pure python shell or executing a non-GUI
            python script, you should use `matplotlib.pyplot.show` instead,
            which takes care of managing the event loop for you.

        Parameters
        ----------
        warn : bool
            If ``True`` and we are not running headless (i.e. on Linux with an
            unset DISPLAY), issue warning when called on a non-GUI backend.
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
        if (backends._get_running_interactive_framework() != "headless"
                and warn):
            cbook._warn_external('Matplotlib is currently using %s, which is '
                                 'a non-GUI backend, so cannot show the '
                                 'figure.' % get_backend())
