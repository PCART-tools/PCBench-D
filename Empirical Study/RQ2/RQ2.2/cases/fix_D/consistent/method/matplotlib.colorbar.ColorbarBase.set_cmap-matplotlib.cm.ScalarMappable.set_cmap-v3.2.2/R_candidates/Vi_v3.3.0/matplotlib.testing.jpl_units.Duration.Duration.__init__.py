    def __init__(self, frame, seconds):
        """
        Create a new Duration object.

        = ERROR CONDITIONS
        - If the input frame is not in the allowed list, an error is thrown.

        = INPUT VARIABLES
        - frame     The frame of the duration.  Must be 'ET' or 'UTC'
        - seconds  The number of seconds in the Duration.
        """
        cbook._check_in_list(self.allowed, frame=frame)
        self._frame = frame
        self._seconds = seconds
