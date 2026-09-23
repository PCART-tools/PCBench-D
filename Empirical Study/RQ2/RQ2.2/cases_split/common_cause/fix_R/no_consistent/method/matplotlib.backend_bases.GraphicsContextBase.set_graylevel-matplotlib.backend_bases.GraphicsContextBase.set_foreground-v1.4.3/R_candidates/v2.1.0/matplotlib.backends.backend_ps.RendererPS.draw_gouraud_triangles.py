    def draw_gouraud_triangles(self, gc, points, colors, trans):
        assert len(points) == len(colors)
        assert points.ndim == 3
        assert points.shape[1] == 3
        assert points.shape[2] == 2
        assert colors.ndim == 3
        assert colors.shape[1] == 3
        assert colors.shape[2] == 4

        shape = points.shape
        flat_points = points.reshape((shape[0] * shape[1], 2))
        flat_points = trans.transform(flat_points)
        flat_colors = colors.reshape((shape[0] * shape[1], 4))
        points_min = np.min(flat_points, axis=0) - (1 << 12)
        points_max = np.max(flat_points, axis=0) + (1 << 12)
        factor = np.ceil(float(2 ** 32 - 1) / (points_max - points_min))

        xmin, ymin = points_min
        xmax, ymax = points_max

        streamarr = np.empty(
            (shape[0] * shape[1],),
            dtype=[('flags', 'u1'),
                   ('points', '>u4', (2,)),
                   ('colors', 'u1', (3,))])
        streamarr['flags'] = 0
        streamarr['points'] = (flat_points - points_min) * factor
        streamarr['colors'] = flat_colors[:, :3] * 255.0

        stream = quote_ps_string(streamarr.tostring())

        self._pswriter.write("""
gsave
<< /ShadingType 4
   /ColorSpace [/DeviceRGB]
   /BitsPerCoordinate 32
   /BitsPerComponent 8
   /BitsPerFlag 8
   /AntiAlias true
   /Decode [ %(xmin)f %(xmax)f %(ymin)f %(ymax)f 0 1 0 1 0 1 ]
   /DataSource (%(stream)s)
>>
shfill
grestore
""" % locals())
