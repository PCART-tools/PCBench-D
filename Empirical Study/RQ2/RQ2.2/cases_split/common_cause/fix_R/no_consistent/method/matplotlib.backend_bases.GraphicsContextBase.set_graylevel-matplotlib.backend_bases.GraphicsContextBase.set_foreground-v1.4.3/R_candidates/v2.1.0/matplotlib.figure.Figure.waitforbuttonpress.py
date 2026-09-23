    def waitforbuttonpress(self, timeout=-1):
        """
        Blocking call to interact with the figure.

        This will return True is a key was pressed, False if a mouse
        button was pressed and None if *timeout* was reached without
        either being pressed.

        If *timeout* is negative, does not timeout.
        """

        blocking_input = BlockingKeyMouseInput(self)
        return blocking_input(timeout=timeout)
