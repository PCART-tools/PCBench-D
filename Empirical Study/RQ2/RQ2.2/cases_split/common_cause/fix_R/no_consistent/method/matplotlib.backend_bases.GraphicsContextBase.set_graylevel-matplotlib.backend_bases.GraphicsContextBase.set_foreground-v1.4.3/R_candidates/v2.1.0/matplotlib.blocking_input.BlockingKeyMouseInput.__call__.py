    def __call__(self, timeout=30):
        """
        Blocking call to retrieve a single mouse or key click
        Returns True if key click, False if mouse, or None if timeout
        """
        self.keyormouse = None
        BlockingInput.__call__(self, n=1, timeout=timeout)

        return self.keyormouse
