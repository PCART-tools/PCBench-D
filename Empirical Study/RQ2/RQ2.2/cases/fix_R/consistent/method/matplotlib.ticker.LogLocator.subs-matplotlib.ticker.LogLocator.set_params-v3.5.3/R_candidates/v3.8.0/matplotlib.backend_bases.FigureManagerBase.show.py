    def show(self):
        """
        For GUI backends, show the figure window and redraw.
        For non-GUI backends, raise an exception, unless running headless (i.e.
        on Linux with an unset DISPLAY); this exception is converted to a
        warning in `.Figure.show`.
        """
        # This should be overridden in GUI backends.
        if sys.platform == "linux" and not os.environ.get("DISPLAY"):
            # We cannot check _get_running_interactive_framework() ==
            # "headless" because that would also suppress the warning when
            # $DISPLAY exists but is invalid, which is more likely an error and
            # thus warrants a warning.
            return
        raise NonGuiException(
            f"{type(self.canvas).__name__} is non-interactive, and thus cannot be "
            f"shown")
