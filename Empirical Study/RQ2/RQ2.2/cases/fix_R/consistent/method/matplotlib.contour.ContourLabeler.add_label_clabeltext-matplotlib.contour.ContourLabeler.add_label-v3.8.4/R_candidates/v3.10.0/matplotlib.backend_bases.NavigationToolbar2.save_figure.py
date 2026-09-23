    def save_figure(self, *args):
        """
        Save the current figure.

        Backend implementations may choose to return
        the absolute path of the saved file, if any, as
        a string.

        If no file is created then `None` is returned.

        If the backend does not implement this functionality
        then `NavigationToolbar2.UNKNOWN_SAVED_STATUS` is returned.

        Returns
        -------
        str or `NavigationToolbar2.UNKNOWN_SAVED_STATUS` or `None`
            The filepath of the saved figure.
            Returns `None` if figure is not saved.
            Returns `NavigationToolbar2.UNKNOWN_SAVED_STATUS` when
            the backend does not provide the information.
        """
        raise NotImplementedError
