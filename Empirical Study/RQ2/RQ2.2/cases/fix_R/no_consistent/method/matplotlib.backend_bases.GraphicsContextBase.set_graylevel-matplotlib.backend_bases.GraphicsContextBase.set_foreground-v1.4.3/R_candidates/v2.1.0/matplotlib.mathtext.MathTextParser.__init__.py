    def __init__(self, output):
        """
        Create a MathTextParser for the given backend *output*.
        """
        self._output = output.lower()
        self._cache = maxdict(50)
