    @classmethod
    def create_with_canvas(cls, canvas_class, figure, num):
        # docstring inherited
        with _restore_foreground_window_at_end():
            if cbook._get_running_interactive_framework() is None:
                cbook._setup_new_guiapp()
                _c_internal_utils.Win32_SetProcessDpiAwareness_max()
            window = tk.Tk(className="matplotlib")
            window.withdraw()

            # Put a Matplotlib icon on the window rather than the default tk
            # icon. See https://www.tcl.tk/man/tcl/TkCmd/wm.html#M50
            #
            # `ImageTk` can be replaced with `tk` whenever the minimum
            # supported Tk version is increased to 8.6, as Tk 8.6+ natively
            # supports PNG images.
            icon_fname = str(cbook._get_data_path(
                'images/matplotlib.png'))
            icon_img = ImageTk.PhotoImage(file=icon_fname, master=window)

            icon_fname_large = str(cbook._get_data_path(
                'images/matplotlib_large.png'))
            icon_img_large = ImageTk.PhotoImage(
                file=icon_fname_large, master=window)
            try:
                window.iconphoto(False, icon_img_large, icon_img)
            except Exception as exc:
                # log the failure (due e.g. to Tk version), but carry on
                _log.info('Could not load matplotlib icon: %s', exc)

            canvas = canvas_class(figure, master=window)
            manager = cls(canvas, num, window)
            if mpl.is_interactive():
                manager.show()
                canvas.draw_idle()
            return manager
