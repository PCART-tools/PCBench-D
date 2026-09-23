    def set_picker(self, picker):
        """
        Set the epsilon for picking used by this artist

        *picker* can be one of the following:

          * *None*: picking is disabled for this artist (default)

          * A boolean: if *True* then picking will be enabled and the
            artist will fire a pick event if the mouse event is over
            the artist

          * A float: if picker is a number it is interpreted as an
            epsilon tolerance in points and the artist will fire
            off an event if it's data is within epsilon of the mouse
            event.  For some artists like lines and patch collections,
            the artist may provide additional data to the pick event
            that is generated, e.g., the indices of the data within
            epsilon of the pick event

          * A function: if picker is callable, it is a user supplied
            function which determines whether the artist is hit by the
            mouse event::

              hit, props = picker(artist, mouseevent)

            to determine the hit test.  if the mouse event is over the
            artist, return *hit=True* and props is a dictionary of
            properties you want added to the PickEvent attributes.

        ACCEPTS: [None|float|boolean|callable]
        """
        self._picker = picker
