    def ginput(self, n=1, timeout=30, show_clicks=True, mouse_add=1,
               mouse_pop=3, mouse_stop=2):
        """
        Blocking call to interact with a figure.

        Wait until the user clicks *n* times on the figure, and return the
        coordinates of each click in a list.

        There are three possible interactions:

        - Add a point.
        - Remove the most recently added point.
        - Stop the interaction and return the points added so far.

        The actions are assigned to mouse buttons via the arguments
        *mouse_add*, *mouse_pop* and *mouse_stop*. Mouse buttons are defined
        by the numbers:

        - 1: left mouse button
        - 2: middle mouse button
        - 3: right mouse button
        - None: no mouse button

        Parameters
        ----------
        n : int, optional, default: 1
            Number of mouse clicks to accumulate. If negative, accumulate
            clicks until the input is terminated manually.
        timeout : scalar, optional, default: 30
            Number of seconds to wait before timing out. If zero or negative
            will never timeout.
        show_clicks : bool, optional, default: True
            If True, show a red cross at the location of each click.
        mouse_add : {1, 2, 3, None}, optional, default: 1 (left click)
            Mouse button used to add points.
        mouse_pop : {1, 2, 3, None}, optional, default: 3 (right click)
            Mouse button used to remove the most recently added point.
        mouse_stop : {1, 2, 3, None}, optional, default: 2 (middle click)
            Mouse button used to stop input.

        Returns
        -------
        points : list of tuples
            A list of the clicked (x, y) coordinates.

        Notes
        -----
        The keyboard can also be used to select points in case your mouse
        does not have one or more of the buttons.  The delete and backspace
        keys act like right clicking (i.e., remove last point), the enter key
        terminates input and any other key (not already used by the window
        manager) selects a point.
        """
        blocking_mouse_input = BlockingMouseInput(self,
                                                  mouse_add=mouse_add,
                                                  mouse_pop=mouse_pop,
                                                  mouse_stop=mouse_stop)
        return blocking_mouse_input(n=n, timeout=timeout,
                                    show_clicks=show_clicks)
