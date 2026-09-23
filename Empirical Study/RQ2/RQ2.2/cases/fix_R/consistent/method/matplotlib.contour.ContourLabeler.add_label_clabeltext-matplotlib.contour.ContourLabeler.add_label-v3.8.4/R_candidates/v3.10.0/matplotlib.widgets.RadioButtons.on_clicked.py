    def on_clicked(self, func):
        """
        Connect the callback function *func* to button click events.

        Parameters
        ----------
        func : callable
            When the button is clicked, call *func* with button label.
            When all buttons are cleared, call *func* with None.
            The callback func must have the signature::

                def func(label: str | None) -> Any

            Return values may exist, but are ignored.

        Returns
        -------
        A connection id, which can be used to disconnect the callback.
        """
        return self._observers.connect('clicked', func)
