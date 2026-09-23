    def writeGouraudTriangles(self):
        gouraudDict = dict()
        for name, points, colors in self.gouraudTriangles:
            ob = self.reserveObject('Gouraud triangle')
            gouraudDict[name] = ob
            shape = points.shape
            flat_points = points.reshape((shape[0] * shape[1], 2))
            flat_colors = colors.reshape((shape[0] * shape[1], 4))
            points_min = np.min(flat_points, axis=0) - (1 << 8)
            points_max = np.max(flat_points, axis=0) + (1 << 8)
            factor = float(0xffffffff) / (points_max - points_min)

            self.beginStream(
                ob.id, None,
                {'ShadingType': 4,
                 'BitsPerCoordinate': 32,
                 'BitsPerComponent': 8,
                 'BitsPerFlag': 8,
                 'ColorSpace': Name('DeviceRGB'),
                 'AntiAlias': True,
                 'Decode': [points_min[0], points_max[0],
                            points_min[1], points_max[1],
                            0, 1, 0, 1, 0, 1]
                 })

            streamarr = np.empty(
                (shape[0] * shape[1],),
                dtype=[(str('flags'), str('u1')),
                       (str('points'), str('>u4'), (2,)),
                       (str('colors'), str('u1'), (3,))])
            streamarr['flags'] = 0
            streamarr['points'] = (flat_points - points_min) * factor
            streamarr['colors'] = flat_colors[:, :3] * 255.0

            self.write(streamarr.tostring())
            self.endStream()
        self.writeObject(self.gouraudObject, gouraudDict)
