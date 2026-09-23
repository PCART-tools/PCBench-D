    def alphaState(self, alpha):
        """Return name of an ExtGState that sets alpha to the given value"""

        state = self.alphaStates.get(alpha, None)
        if state is not None:
            return state[0]

        name = Name('A%d' % self.nextAlphaState)
        self.nextAlphaState += 1
        self.alphaStates[alpha] = \
            (name, {'Type': Name('ExtGState'),
                    'CA': alpha[0], 'ca': alpha[1]})
        return name
