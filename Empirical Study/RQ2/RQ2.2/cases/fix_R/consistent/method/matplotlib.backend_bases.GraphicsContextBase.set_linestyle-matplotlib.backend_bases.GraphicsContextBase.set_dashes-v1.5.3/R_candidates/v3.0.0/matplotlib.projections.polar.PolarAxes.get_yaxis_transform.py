    def get_yaxis_transform(self, which='grid'):
        if which in ('tick1', 'tick2'):
            return self._yaxis_text_transform
        elif which == 'grid':
            return self._yaxis_transform
        else:
            raise ValueError(
                "'which' must be one of 'tick1', 'tick2', or 'grid'")
