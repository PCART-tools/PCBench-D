    def __init__(self, n=None):
        """
        *n* is the number of subdivisions of the interval between
        major ticks; e.g., n=2 will place a single minor tick midway
        between major ticks.

        If *n* is omitted or None, the value stored in rcParams will be used.
        In case *n* is set to 'auto', it will be set to 4 or 5. If the distance
        between the major ticks equals 1, 2.5, 5 or 10 it can be perfectly
        divided in 5 equidistant sub-intervals with a length multiple of
        0.05. Otherwise it is divided in 4 sub-intervals.
        """
        self.ndivs = n
