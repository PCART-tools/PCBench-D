    def __str__(self):
        if self.a == self.b:
            r = self.a
        else:
            r = (self.a, self.b)

        return "Annulus(xy=(%s, %s), r=%s, width=%s, angle=%s)" % \
                (*self.center, r, self.width, self.angle)
