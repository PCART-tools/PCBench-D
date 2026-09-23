    def __call__(self, timeout=30):
        """
        Blocking call to retrieve a single mouse click or key press.

        Returns ``True`` if key press, ``False`` if mouse click, or ``None`` if
        timed out.
        """
        self.keyormouse = None
        super().__call__(n=1, timeout=timeout)

        return self.keyormouse
