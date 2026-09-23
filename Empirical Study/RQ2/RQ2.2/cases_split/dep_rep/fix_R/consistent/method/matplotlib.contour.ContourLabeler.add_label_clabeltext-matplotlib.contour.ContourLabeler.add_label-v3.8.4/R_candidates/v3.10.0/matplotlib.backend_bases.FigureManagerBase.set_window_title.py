    def set_window_title(self, title):
        """
        Set the title text of the window containing the figure.

        This has no effect for non-GUI (e.g., PS) backends.

        Examples
        --------
        >>> fig = plt.figure()
        >>> fig.canvas.manager.set_window_title('My figure')
        """
