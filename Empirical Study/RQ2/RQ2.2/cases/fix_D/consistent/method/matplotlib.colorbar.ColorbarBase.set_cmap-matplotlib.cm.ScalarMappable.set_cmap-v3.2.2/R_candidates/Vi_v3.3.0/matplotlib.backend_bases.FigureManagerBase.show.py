    def show(self):
        """
        For GUI backends, show the figure window and redraw.
        For non-GUI backends, raise an exception, unless running headless (i.e.
        on Linux with an unset DISPLAY); this exception is converted to a
        warning in `.Figure.show`.
        """
        # This should be overridden in GUI backends.
        if cbook._get_running_interactive_framework() != "headless":
            raise NonGuiException(
                f"Matplotlib is currently using {get_backend()}, which is "
                f"a non-GUI backend, so cannot show the figure.")
