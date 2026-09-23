    def _text_y(self, y):
        if self.labelpos == 'N':
            return y + self.labelsep
        elif self.labelpos == 'S':
            return y - self.labelsep
        else:
            return y
