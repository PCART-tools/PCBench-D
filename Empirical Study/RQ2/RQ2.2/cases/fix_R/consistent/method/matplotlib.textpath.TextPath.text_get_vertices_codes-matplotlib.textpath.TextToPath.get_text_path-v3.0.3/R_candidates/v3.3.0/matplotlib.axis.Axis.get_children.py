    def get_children(self):
        return [self.label, self.offsetText,
                *self.get_major_ticks(), *self.get_minor_ticks()]
