    def _text_x(self, x):
        if self.labelpos == 'E':
            return x + self.labelsep
        elif self.labelpos == 'W':
            return x - self.labelsep
        else:
            return x
