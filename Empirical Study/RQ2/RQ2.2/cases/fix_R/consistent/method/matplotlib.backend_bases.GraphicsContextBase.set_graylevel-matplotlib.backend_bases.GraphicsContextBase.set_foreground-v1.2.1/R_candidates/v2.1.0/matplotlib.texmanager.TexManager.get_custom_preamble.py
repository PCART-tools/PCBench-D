    def get_custom_preamble(self):
        """returns a string containing user additions to the tex preamble"""
        return '\n'.join(rcParams['text.latex.preamble'])
