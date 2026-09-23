    @cbook.deprecated("3.1")
    def shouldstroke(self):
        return (self.get_linewidth() > 0.0 and
                (len(self.get_rgb()) <= 3 or self.get_rgb()[3] != 0.0))
