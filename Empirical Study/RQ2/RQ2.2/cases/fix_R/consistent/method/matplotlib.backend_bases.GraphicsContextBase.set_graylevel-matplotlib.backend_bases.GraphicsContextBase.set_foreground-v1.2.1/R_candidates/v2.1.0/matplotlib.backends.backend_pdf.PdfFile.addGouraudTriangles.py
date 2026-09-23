    def addGouraudTriangles(self, points, colors):
        name = Name('GT%d' % len(self.gouraudTriangles))
        self.gouraudTriangles.append((name, points, colors))
        return name
