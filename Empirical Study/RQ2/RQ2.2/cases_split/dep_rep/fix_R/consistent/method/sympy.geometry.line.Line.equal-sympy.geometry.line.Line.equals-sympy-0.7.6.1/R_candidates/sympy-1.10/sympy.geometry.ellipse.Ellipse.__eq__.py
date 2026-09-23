    def __eq__(self, o):
        """Is the other GeometryEntity the same as this ellipse?"""
        return isinstance(o, Ellipse) and (self.center == o.center and
                                           self.hradius == o.hradius and
                                           self.vradius == o.vradius)
