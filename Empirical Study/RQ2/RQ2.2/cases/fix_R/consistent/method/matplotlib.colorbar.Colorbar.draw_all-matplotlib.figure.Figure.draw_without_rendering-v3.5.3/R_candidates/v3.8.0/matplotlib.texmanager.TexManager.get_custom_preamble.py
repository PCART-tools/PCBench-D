    @classmethod
    def get_custom_preamble(cls):
        """Return a string containing user additions to the tex preamble."""
        return mpl.rcParams['text.latex.preamble']
