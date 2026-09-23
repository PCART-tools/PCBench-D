    @classmethod
    def new_figure_manager_given_figure(cls, num, figure):
        """
        Create a new figure manager instance for the given figure.
        """
        with _restore_foreground_window_at_end():
            if cbook._get_running_interactive_framework() is None:
                cbook._setup_new_guiapp()
                _c_internal_utils.Win32_SetProcessDpiAwareness_max()
            window = tk.Tk(className="matplotlib")
            window.withdraw()

            # Put a Matplotlib icon on the window rather than the default tk
            # icon.  Tkinter doesn't allow colour icons on linux systems, but
            # tk>=8.5 has a iconphoto command which we call directly.  See
            # https://mail.python.org/pipermail/tkinter-discuss/2006-November/000954.html
            icon_fname = str(cbook._get_data_path(
                'images/matplotlib_128.ppm'))
            icon_img = tk.PhotoImage(file=icon_fname, master=window)
            try:
                window.iconphoto(False, icon_img)
            except Exception as exc:
                # log the failure (due e.g. to Tk version), but carry on
                _log.info('Could not load matplotlib icon: %s', exc)

            canvas = cls.FigureCanvas(figure, master=window)
            manager = cls.FigureManager(canvas, num, window)
            if mpl.is_interactive():
                manager.show()
                canvas.draw_idle()
            return manager
