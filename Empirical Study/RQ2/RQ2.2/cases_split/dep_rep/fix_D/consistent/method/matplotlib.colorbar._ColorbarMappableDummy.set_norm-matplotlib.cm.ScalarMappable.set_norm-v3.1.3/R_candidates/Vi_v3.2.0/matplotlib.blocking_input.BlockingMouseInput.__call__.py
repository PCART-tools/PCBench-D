    def __call__(self, n=1, timeout=30, show_clicks=True):
        """
        Blocking call to retrieve *n* coordinate pairs through mouse clicks.
        """
        self.show_clicks = show_clicks
        self.clicks = []
        self.marks = []
        BlockingInput.__call__(self, n=n, timeout=timeout)
        return self.clicks
