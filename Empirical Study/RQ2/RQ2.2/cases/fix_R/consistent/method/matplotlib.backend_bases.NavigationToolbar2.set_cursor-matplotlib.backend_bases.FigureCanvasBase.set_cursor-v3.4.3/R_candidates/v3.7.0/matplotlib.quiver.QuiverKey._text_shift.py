    def _text_shift(self):
        return {
            "N": (0, +self.labelsep),
            "S": (0, -self.labelsep),
            "E": (+self.labelsep, 0),
            "W": (-self.labelsep, 0),
        }[self.labelpos]
