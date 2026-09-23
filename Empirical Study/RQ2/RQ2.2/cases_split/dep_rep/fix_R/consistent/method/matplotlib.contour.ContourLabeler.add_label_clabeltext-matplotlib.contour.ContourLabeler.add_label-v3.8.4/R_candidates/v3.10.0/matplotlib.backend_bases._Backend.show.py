    @classmethod
    def show(cls, *, block=None):
        """
        Show all figures.

        `show` blocks by calling `mainloop` if *block* is ``True``, or if it is
        ``None`` and we are not in `interactive` mode and if IPython's
        ``%matplotlib`` integration has not been activated.
        """
        managers = Gcf.get_all_fig_managers()
        if not managers:
            return
        for manager in managers:
            try:
                manager.show()  # Emits a warning for non-interactive backend.
            except NonGuiException as exc:
                _api.warn_external(str(exc))
        if cls.mainloop is None:
            return
        if block is None:
            # Hack: Is IPython's %matplotlib integration activated?  If so,
            # IPython's activate_matplotlib (>= 0.10) tacks a _needmain
            # attribute onto pyplot.show (always set to False).
            pyplot_show = getattr(sys.modules.get("matplotlib.pyplot"), "show", None)
            ipython_pylab = hasattr(pyplot_show, "_needmain")
            block = not ipython_pylab and not is_interactive()
        if block:
            cls.mainloop()
